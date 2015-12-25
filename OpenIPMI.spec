#
# Conditional build:
%bcond_without	gui	# don't build tkinter-based GUI
#
Summary:	IPMI abstraction layer
Summary(pl.UTF-8):	Warstwa abstrakcji IPMI
Name:		OpenIPMI
Version:	2.0.21
Release:	5
License:	LGPL v2+ (library), GPL v2+ (ipmicmd)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
# Source0-md5:	dc0b42ae40b3f1d0db2a94b75b95fae1
Patch0:		%{name}-link.patch
Patch1:		%{name}-pthread.patch
Patch2:		avoid-echo-e.patch
Patch3:		%{name}-ac.patch
URL:		http://openipmi.sourceforge.net/
BuildRequires:	autoconf >= 2.50
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
BuildRequires:	python-devel
%{?with_gui:BuildRequires:	python-tkinter}
BuildRequires:	tcl-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-perl >= 1.3.25
BuildRequires:	swig-python >= 1.3.25
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

%package -n python-%{name}
Summary:	Python interface to OpenIPMI
Summary(pl.UTF-8):	Pythonowy interfejs do OpenIPMI
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-%{name}
Python interface to OpenIPMI.

%description -n python-%{name} -l pl.UTF-8
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
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	--with-pythoninstall=%{py_sitescriptdir} \
	--with-pythoninstalllib=%{py_sitedir} \
	--without-glib12 \
	%{!?with_gui:--without-tkinter}
%{__make} %{?with_gui:-j1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a} \
	$RPM_BUILD_ROOT%{py_sitescriptdir}/*.py \
	%{?with_gui:$RPM_BUILD_ROOT%{py_sitescriptdir}/openipmigui/*.py}

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
%{_includedir}/%{name}
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

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_OpenIPMI.so
%{py_sitescriptdir}/OpenIPMI.py[co]

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%doc swig/python/openipmigui/TODO
%attr(755,root,root) %{_bindir}/openipmigui
%dir %{py_sitescriptdir}/openipmigui
%{py_sitescriptdir}/openipmigui/*.py[co]
%{_mandir}/man1/openipmigui.1*
%endif
