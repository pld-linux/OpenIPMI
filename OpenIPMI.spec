%include	/usr/lib/rpm/macros.perl
Summary:	IPMI abstraction layer
Name:		OpenIPMI
Version:	1.1.5
Release:	1
License:	Apache-style License
Group:		Libraries
Source0:	http://dl.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
# Source0-md5:	133fc7a56b815c4f1b64bd790a0d0dc6
URL:		http://openipmi.sourceforge.net/
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open IPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface
(IPMI).

%package devel
Summary:	Development part of OpenIPMI Toolkit libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development part of OpenIPMI library.

%package static
Summary:	Static OpenIPMI libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static OpenIPMI Toolkit libraries.

# this is workaround only, to be removed in future
%define		no_install_post_strip	1

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CPPFLAGS="-I%{_includedir}/ncurses";
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%doc ChangeLog FAQ README* TODO
%attr(755,root,root) %{_bindir}/*
%{_infodir}/%{name}*
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
