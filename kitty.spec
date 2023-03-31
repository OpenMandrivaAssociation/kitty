%define _empty_manifest_terminate_build 0
%global __python %{__python3}

Name: kitty
Summary: Fast, featureful, GPU based terminal emulator
Version:	0.27.1
Release:	2
Group: System/X11
License: GPLv3
URL: https://github.com/kovidgoyal/kitty
Source0: https://github.com/kovidgoyal/kitty/releases/download/v%{version}/kitty-%{version}.tar.xz

BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinx-inline-tabs)
BuildRequires:  imagemagick-devel
BuildRequires:  librsync-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  golang
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(libpng)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcanberra)

%description
Kitty supports modern terminal features like: graphics, unicode,
true-color, OpenType ligatures, mouse protocol, focus tracking, and
bracketed paste.

Kitty has a framework for "kittens", small terminal programs that can be used
to extend its functionality.

%package doc
Summary:        Documentation for the kitty terminal emulator
License:        GPLv3

%description doc
Documentation for the kitty terminal emulator

%prep
%autosetup -p1

%build
#export CC=%{__cc}
# The --debug option has been removed as it caused 
# the app launcher to be improperly linked.
# The problem it causes shows up in the fact that the kitty.conf file is
# not generated although the app runs. Debug rpms are still produced.

%{__python3} setup.py linux-package  --libdir-name %{_lib} 

%install
install -d %{buildroot}/usr
cp -a linux-package/* %{buildroot}/usr

%files
%{_bindir}/%{name}
%{_bindir}/kitten
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/kitty-open.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/kitty.svg
%{_datadir}/terminfo/x/xterm-kitty
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/kitty.conf.5.*

%files doc
%doc LICENSE *.md *.rst *.asciidoc
%{_docdir}/kitty/html
