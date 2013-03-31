#!/usr/bin/clisp

(defparameter decay 100)
(defparameter t1 1)
(defparameter t2 1)

(defun pulse (n)
  (setf decay 200)
  (print 'beat)
  ;(print n)
  (setf t2 t1)
  (setf t1 n)
  (print (- t1 t2))
)

(defun foo (b n)
  (setf decay (1- decay))
  (if (and (< decay 0) (> b 220)) (pulse n) ())
)

(defun read-audio (file)
  (with-open-file (in file :element-type '(unsigned-byte 8))
   (loop
     for b = (read-byte in nil nil)
     for n from 1 
     while b
     do(foo b n)
   )
  )
)


(read-audio "click.wav")
