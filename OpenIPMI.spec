# TODO
# - bad BR (version mismatch):
#  File "_mc_user.py", line 240, in ?
#    class MCUsers(gui_treelist.TreeList): AttributeError: 'module' object has no attribute 'TreeList'
#  make[4]: *** [_entity.pyc] Error 1
#
# Conditional build:
%bcond_without	gui	# don't build tkinter-based GUI
#
Summary:	IPMI abstraction layer
Summary(pl.UTF-8):	Warstwa abstrakcji IPMI
Name:		OpenIPMI
Version:	2.0.10
Release:	2
License:	LGPL (library), GPL (ipmicmd)
Group:		Libraries
Source0:	http://dl.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
# Source0-md5:	8f5c200c5f25c33250567eaeb685e8c0
Patch0:		%{name}-link.patch
Patch1:		%{name}-python.patch
URL:		http://openipmi.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gdbm-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-devel
%{?with_gui:BuildRequires:	python-tkinter}
BuildRequires:	tcl-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-perl >= 1.3.25
BuildRequires:	swig-python >= 1.3.25
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenIPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface
(IPMI).

%description -l pl.UTF-8
Celem projektu OpenIPMI jest stworzenie otwartej podstawy kodu
pozwalającego na dostęp do informacji o platformie pzy użyciu
interfejsu IPMI (Intelligent Platform Management Interface -
interfejsu inteligentnego zarządzania platformą)

%package devel
Summary:	Development part of OpenIPMI Toolkit libraries
Summary(pl.UTF-8):	Programistyczna cześć bibliotek OpenIPMI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development part of OpenIPMI libraries.

%description devel -l pl.UTF-8
Programistyczna cześć bibliotek OpenIPMI.

%package static
Summary:	Static OpenIPMI libraries
Summary(pl.UTF-8):	Statyczne biblioteki OpenIPMI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenIPMI Toolkit libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenIPMI.

%package -n perl-%{name}
Summary:	Perl interface to OpenIPMI
Summary(pl.UTF-8):	Perlowy interfejs do OpenIPMI
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl interface to OpenIPMI.

%description -n perl-%{name} -l pl.UTF-8
Perlowy interfejs do OpenIPMI.

%package -n python-%{name}
Summary:	Python interface to OpenIPMI
Summary(pl.UTF-8):	Pythonowy interfejs do OpenIPMI
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-%{name}
Python interface to OpenIPMI.

%description -n perl-%{name} -l pl.UTF-8
Pythonowy interfejs do OpenIPMI.

%package gui
Summary:	OpenIPMI GUI
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do OpenIPMI
Group:		X11/Applications
Requires:	python-%{name} = %{version}-%{release}
Requires:	python-tkinter

%description gui
OpenIPMI GUI.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika do OpenIPMI.

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
%configure \
	--without-glib12 \
	%{!?with_gui:--without-tkinter}
%{__make} \
	PYTHON_INSTALL_DIR=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \
	PYTHON_INSTALL_DIR=%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a} \
	$RPM_BUILD_ROOT%{py_sitedir}/openipmigui/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README* TODO
%attr(755,root,root) %{_bindir}/ipmi*
%attr(755,root,root) %{_bindir}/openipmicmd
%attr(755,root,root) %{_bindir}/openipmish
%attr(755,root,root) %{_bindir}/rmcp_ping
%attr(755,root,root) %{_bindir}/solterm
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

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_OpenIPMI.so
%{py_sitedir}/OpenIPMI.py[co]

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%doc swig/python/openipmigui/TODO
%attr(755,root,root) %{_bindir}/openipmigui
%dir %{py_sitedir}/openipmigui
%{py_sitedir}/openipmigui/*.py[co]
%endif
