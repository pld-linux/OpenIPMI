Summary:	IPMI abstraction layer
Summary(pl):	Warstwa abstrakcji IPMI
Name:		OpenIPMI
Version:	1.4.7
Release:	1
License:	LGPL (library), GPL (ipmicmd)
Group:		Libraries
Source0:	http://dl.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
# Source0-md5:	288dfcc7d1de18783e9066bb82204c54
Patch0:		%{name}-link.patch
Patch1:		%{name}-headers.patch
URL:		http://openipmi.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenIPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface
(IPMI).

%description -l pl
Celem projektu OpenIPMI jest stworzenie otwartej podstawy kodu
pozwalaj�cego na dost�p do informacji o platformie pzy u�yciu
interfejsu IPMI (Intelligent Platform Management Interface -
interfejsu inteligentnego zarz�dzania platform�)

%package devel
Summary:	Development part of OpenIPMI Toolkit libraries
Summary(pl):	Programistyczna cze�� bibliotek OpenIPMI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development part of OpenIPMI libraries.

%description devel -l pl
Programistyczna cze�� bibliotek OpenIPMI.

%package static
Summary:	Static OpenIPMI libraries
Summary(pl):	Statyczne biblioteki OpenIPMI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenIPMI Toolkit libraries.

%description static -l pl
Statyczne biblioteki OpenIPMI.

%package -n perl-%{name}
Summary:	Perl interface to OpenIPMI
Summary(pl):	Perlowy interfejs do OpenIPMI
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl interface to OpenIPMI.

%description -n perl-%{name} -l pl
Perlowy interfejs do OpenIPMI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CPPFLAGS="-I/usr/include/ncurses"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README* TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man[178]/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/OpenIPMI.pm
%dir %{perl_vendorarch}/auto/OpenIPMI
%attr(755,root,root) %{perl_vendorarch}/auto/OpenIPMI/OpenIPMI.so