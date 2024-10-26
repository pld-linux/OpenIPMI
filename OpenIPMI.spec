#
# Conditional build:
%bcond_without	gui	# tkinter-based GUI
#
Summary:	IPMI abstraction layer
Summary(pl.UTF-8):	Warstwa abstrakcji IPMI
Name:		OpenIPMI
Version:	2.0.36
Release:	1
License:	LGPL v2+ (library), GPL v2+ (ipmicmd)
Group:		Libraries
Source0:	https://downloads.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
# Source0-md5:	e77028dcfb6e91cc256da19723af1a2e
Patch0:		%{name}-tcl.patch
URL:		http://openipmi.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	autoconf-archive >= 2017.03.21
BuildRequires:	automake
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gdbm-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules
%{?with_gui:BuildRequires:	python3-tkinter}
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-perl >= 1.3.25
BuildRequires:	swig-python >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libOpenIPMIcmdlang refers to global ipmi_cmdlang_{global_err,report_event} symbols
# libIPMIlanserv uses symbols from binaries (ipmilan, ipmi_sim)
%define		skip_post_check_so	libOpenIPMIcmdlang\.so\..* libIPMIlanserv\.so\..*

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

%package -n python3-%{name}
Summary:	Python interface to OpenIPMI
Summary(pl.UTF-8):	Pythonowy interfejs do OpenIPMI
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-OpenIPMI < 2.0.32

%description -n python3-%{name}
Python interface to OpenIPMI.

%description -n python3-%{name} -l pl.UTF-8
Pythonowy interfejs do OpenIPMI.

%package gui
Summary:	OpenIPMI GUI
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do OpenIPMI
Group:		X11/Applications
Requires:	python3-%{name} = %{version}-%{release}
Requires:	python3-tkinter

%description gui
OpenIPMI GUI.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika do OpenIPMI.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' swig/python/openipmigui.py
%{__rm} m4/ax_python_devel.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	PYTHON=%{__python3} \
	--with-pythoninstall=%{py3_sitescriptdir} \
	--with-pythoninstalllib=%{py3_sitedir} \
	--with-tkinter%{!?with_gui:=no}
%{__make} %{?with_gui:-j1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONFIGURING_FOR_LAN ChangeLog FAQ README* TODO
%attr(755,root,root) %{_bindir}/ipmi_sim
%attr(755,root,root) %{_bindir}/ipmi_ui
%attr(755,root,root) %{_bindir}/ipmicmd
%attr(755,root,root) %{_bindir}/ipmilan
%attr(755,root,root) %{_bindir}/ipmish
%attr(755,root,root) %{_bindir}/openipmi_eventd
%attr(755,root,root) %{_bindir}/openipmicmd
%attr(755,root,root) %{_bindir}/openipmish
%attr(755,root,root) %{_bindir}/rmcp_ping
%attr(755,root,root) %{_bindir}/sdrcomp
%attr(755,root,root) %{_bindir}/solterm
%attr(755,root,root) %{_libdir}/libIPMIlanserv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIPMIlanserv.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMI.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMI.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMIcmdlang.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIcmdlang.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMIglib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIglib.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMIposix.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIposix.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMIpthread.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIpthread.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMItcl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMItcl.so.0
%attr(755,root,root) %{_libdir}/libOpenIPMIui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIui.so.1
%attr(755,root,root) %{_libdir}/libOpenIPMIutils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenIPMIutils.so.0
%dir %{_sysconfdir}/ipmi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipmi/ipmisim1.emu
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipmi/lan.conf
%{_mandir}/man1/ipmi_sim.1*
%{_mandir}/man1/ipmi_ui.1*
%{_mandir}/man1/openipmi_eventd.1*
%{_mandir}/man1/openipmicmd.1*
%{_mandir}/man1/openipmish.1*
%{_mandir}/man1/rmcp_ping.1*
%{_mandir}/man1/solterm.1*
%{_mandir}/man5/ipmi_lan.5*
%{_mandir}/man5/ipmi_sim_cmd.5*
%{_mandir}/man7/ipmi_cmdlang.7*
%{_mandir}/man7/openipmi_conparms.7*
%{_mandir}/man8/ipmilan.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libIPMIlanserv.so
%attr(755,root,root) %{_libdir}/libOpenIPMI.so
%attr(755,root,root) %{_libdir}/libOpenIPMIcmdlang.so
%attr(755,root,root) %{_libdir}/libOpenIPMIglib.so
%attr(755,root,root) %{_libdir}/libOpenIPMIposix.so
%attr(755,root,root) %{_libdir}/libOpenIPMIpthread.so
%attr(755,root,root) %{_libdir}/libOpenIPMItcl.so
%attr(755,root,root) %{_libdir}/libOpenIPMIui.so
%attr(755,root,root) %{_libdir}/libOpenIPMIutils.so
%{_libdir}/libIPMIlanserv.la
%{_libdir}/libOpenIPMI.la
%{_libdir}/libOpenIPMIcmdlang.la
%{_libdir}/libOpenIPMIglib.la
%{_libdir}/libOpenIPMIposix.la
%{_libdir}/libOpenIPMIpthread.la
%{_libdir}/libOpenIPMItcl.la
%{_libdir}/libOpenIPMIui.la
%{_libdir}/libOpenIPMIutils.la
%{_includedir}/OpenIPMI
%{_pkgconfigdir}/OpenIPMI.pc
%{_pkgconfigdir}/OpenIPMIcmdlang.pc
%{_pkgconfigdir}/OpenIPMIglib.pc
%{_pkgconfigdir}/OpenIPMIposix.pc
%{_pkgconfigdir}/OpenIPMIpthread.pc
%{_pkgconfigdir}/OpenIPMItcl.pc
%{_pkgconfigdir}/OpenIPMIui.pc
%{_pkgconfigdir}/OpenIPMIutils.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libIPMIlanserv.a
%{_libdir}/libOpenIPMI.a
%{_libdir}/libOpenIPMIcmdlang.a
%{_libdir}/libOpenIPMIglib.a
%{_libdir}/libOpenIPMIposix.a
%{_libdir}/libOpenIPMIpthread.a
%{_libdir}/libOpenIPMItcl.a
%{_libdir}/libOpenIPMIui.a
%{_libdir}/libOpenIPMIutils.a

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/OpenIPMI.pm
%dir %{perl_vendorarch}/auto/OpenIPMI
%attr(755,root,root) %{perl_vendorarch}/auto/OpenIPMI/OpenIPMI.so

%files -n python3-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_OpenIPMI.so
%{py3_sitescriptdir}/OpenIPMI.py
%{py3_sitescriptdir}/__pycache__/OpenIPMI.cpython-*.py[co]

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%doc swig/python/openipmigui/TODO
%attr(755,root,root) %{_bindir}/openipmigui
%{py3_sitescriptdir}/openipmigui
%{_mandir}/man1/openipmigui.1*
%endif
