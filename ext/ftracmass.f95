subroutine file_open(fd, filename)
    INTEGER :: fd
	CHARACTER(LEN=*) :: filename
	print *, 'file open :', fd, len(filename), trim(filename)	
    open(unit=fd, file=trim(filename))

	
end subroutine file_open


subroutine simple_print()
	use mod_time
	IMPLICIT none
	print *, 'intend :', LOC(intend)
	print *, 'intend :', intend
	
	intend = 99
	print *, 'intend :', intend

	

end subroutine simple_print

