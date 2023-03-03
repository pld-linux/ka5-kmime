#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.12.3
%define		qtver		5.15.2
%define		kaname		kmime
Summary:	KMime
Name:		ka5-%{kaname}
Version:	22.12.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	875fa04e557bfb9752d6709cd8e18e44
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= 5.9.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.53.0
BuildRequires:	kf5-kcodecs-devel >= 5.51.0
BuildRequires:	kf5-ki18n-devel
BuildRequires:	kf5-ki18n-devel >= 5.51.0
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KMime is a library for handling mail messages and newsgroup articles.
Both mail messages and newsgroup articles are based on the same
standard called MIME, which stands for
- **Multipurpose Internet Mail Extensions**. In this document, the
  term `message` is used to refer to both mail messages and newsgroup
  articles.

%description -l pl.UTF-8
KMime jest biblioteką do obsługi wiadomości pocztowych i artykułów
grup Usenetowych. Zarówno wiadomości pocztowe i artykuły są oparte na
tym samym standardzie zwanym MIME
- **Multipurpose Internet Mail Extensions**, (**Uniweralne
  roszszerzenie poczty internetowej**). W tym dokumencie, termin
  `wiadomość` oznacza zarówno wiadomości pocztowe, jak i artykuły grup
  news.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libKF5Mime.so.5
%attr(755,root,root) %{_libdir}/libKF5Mime.so.*.*.*
%{_datadir}/qlogging-categories5/kmime.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KMime
%{_libdir}/cmake/KF5Mime
%{_libdir}/libKF5Mime.so
%{_libdir}/qt5/mkspecs/modules/qt_KMime.pri
