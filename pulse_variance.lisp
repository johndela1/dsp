#!/usr/bin/clisp

(defparameter *t1* (get-internal-real-time))
(defparameter *t2* 1)
(defparameter *avg* (cons 1 1))
(defparameter *var* (cons 1 1))
(defparameter *factor* .25)

(defun exp_decay (new_num cur_avg fact)
 (+ (* new_num fact) (* cur_avg (- 1 fact))))

(defun calc_variance (key)
 (setf *t2* *t1*)
 (setf *t1* (get-internal-real-time))
 (setf delta (- *t1* *t2*))
 (if (eql key #\Return)
  (progn (setf (cdr *avg*) (exp_decay delta (cdr *avg*) *factor*))
   (setf (cdr *var*)
    (exp_decay (abs (- (cdr *avg*) delta)) (cdr *var*) *factor*)))
  (progn (setf (car *avg*) (exp_decay delta (car *avg*) *factor*))
   (setf (car *var*)
    (exp_decay (abs (- (car *avg*) delta)) (car *var*) *factor*)))
 )
 (print 'left)
 ;(print (round (/ (car *avg*) 1000)))
 (print (round (/ (car *var*) 1000)))
 (print 'right)
 ;(print (round (/ (cdr *avg*) 1000)))
 (print (round (/ (cdr *var*) 1000)))
 (print '-------)
)

(EXT:WITH-KEYBOARD
 (print 'spacebar_to_exit)
 (LOOP :for char = (READ-CHAR EXT:*KEYBOARD-INPUT*)
   :for key = (OR (EXT:CHAR-KEY char) (CHARACTER char))
   :do (calc_variance key)
   :when (EQL key #\Space) :return (LIST char key)))

