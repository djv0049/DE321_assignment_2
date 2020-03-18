# $Id: CMakeLists.txt,v 1.4 2006/07/09 04:29:49 ellson Exp $ $Revision: 1.4 $

INCLUDE(SRCDIRs)
INCLUDE(${gd_SRCDIR}/sources.cmake)

# rename private copy of libgd to libgvgd
SET(gvgd_SRCS ${gd_SRCS})

ADD_LIBRARY(gvgd STATIC ${gvgd_SRCS})

INSTALL_FILES(FILES
	gd.html
)
