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


subroutine get_uflux_shape(uflux_shape)
    use mod_vel
	INTEGER :: uflux_shape(4)
	
	uflux_shape = shape(uflux)

end subroutine get_uflux_shape

subroutine get_vflux_shape(a_shape)
    use mod_vel
	INTEGER :: a_shape(4)
	a_shape = shape(vflux)

end subroutine get_vflux_shape