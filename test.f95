module mod_fu

    REAL*4, ALLOCATABLE, DIMENSION(:)    :: uflux

end module mod_fu

SUBROUTINE testcase(i)
	use mod_fu
	INTEGER :: i
	
	ALLOCATE (uflux(0:i))
	
	print *, 'LOC', LOC(uflux)
	print *, 'SHAPE', SHAPE(uflux),'+'
	
	call shapeof()
	uflux(0) = 1
	uflux(1) = 2
	uflux(2) = 3
		

end SUBROUTINE testcase


SUBROUTINE shapeof()
	print *, 'SHAPE', SHAPE(uflux(:1)), ';'
	
end SUBROUTINE shapeof
