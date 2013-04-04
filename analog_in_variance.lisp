#!/usr/bin/clisp

(defparameter decay 100)
(defparameter *t1* (get-internal-real-time))
(defparameter *t2* 1)
(defparameter *avg* (cons 1 1))
(defparameter *var* (cons 1 1))
(defparameter *factor* .5)
(defparameter *last-n* 0)

(defun pulse (n)
  (setf decay 10000)
  (print 'bpm)
  (print (* 957000.0 (/ 1 (- n *last-n*))))
  (print 'bpm-based-on-clock)
  (print (/ 60000000.0 (- *t1* *t2*)))
  (setf *last-n* n)
  (calc-variance 'f)
)

(defun sample (amplitude n)
  (setf decay (1- decay))
  (if (and (< decay 0) (> amplitude 190)) (pulse n) ())
)

(defun read-audio (in)
   (loop
     for b = (read-byte in nil nil)
     for n from 1 
     while b
     do(sample b n)
   )
)

(defun exp_decay (new_num cur_avg fact)
 (+ (* new_num fact) (* cur_avg (- 1 fact))))

(defun calc-variance (key)
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
 (print (round (/ (car *var*) 1000)))
 (print 'right)
 (print (round (/ (cdr *var*) 1000)))
 (print '-------)
)

(setf (stream-element-type *standard-input*) '(unsigned-byte 8)) 
(read-audio *standard-input*)
(EXT:WITH-KEYBOARD
 (print 'spacebar_to_exit)
 (LOOP :for char = (READ-CHAR EXT:*KEYBOARD-INPUT*)
   :for key = (OR (EXT:CHAR-KEY char) (CHARACTER char))
   :do (calc-variance key)
   :when (EQL key #\Space) :return (LIST char key)))

