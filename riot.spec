# To avoid out of memory error
%define _build_pkgcheck_set %{nil}

%define debug_package %{nil}

%define oname riot-web
%define _riotdir /opt/riot

%define __noautoreqfiles /opt/riot/resources
%define __noautoreq 'libffmpeg.so*|libnode.so*'

Summary:	Client for the decentralized and secure protocol Matrix
Name:		riot
Version:	0.15.5
Release:	1
License:	ASL 2.0
Group:		Networking/Instant messaging
Url:		http://riot.im/
Source0:	https://github.com/vector-im/riot-web/releases/download/v0.15.5/riot-v0.15.5.tar.gz
#Source1:	%{name}-extras-desktop.tar.gz
#Patch0:		riot-web-0.15.4-menubar.patch
#Patch1:		riot-web-0.15.5-kde-tray-icon.patch
BuildRequires:	git
BuildRequires:	nodejs
AutoProv:	no

%description
Riot is a decentralized, secure messaging client for collaborative group
communication. Riot's core architecture is an implementation of the Matrix
protocol.

Riot is more than a messaging app. Riot is a shared workspace for the web.
Riot is a place to connect with teams. Riot is a place to to collaborate,
to work, to discuss your current projects.

Riot removes the barriers between apps, allowing you to connect teams and
functionality like never before.

Riot is free. Riot is secure.

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_riotdir}/*

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-v%{version}
#patch0 -p1
#patch1 -p1

%build
npm install
npm run build

%ifarch x86_64
%define linuxunpacked electron_app/dist/linux-unpacked
node_modules/.bin/build -l tar.gz --x64
%else
%define linuxunpacked electron_app/dist/linux-ia32-unpacked
node_modules/.bin/build -l tar.gz --ia32
%endif

%install
mkdir -p %{buildroot}%{_riotdir}
cp -a %{linuxunpacked}/* %{buildroot}%{_riotdir}

# install binary wrapper
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/riot << EOF
#!/bin/sh
pushd %{_riotdir}
./riot-web
popd
EOF
chmod 755 %{buildroot}%{_bindir}/riot

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Riot
Comment=Client for the decentralized and secure protocol Matrix
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Network;InstantMessaging;
EOF

# install menu icons
for N in 16 22 24 32 48 128 256;
do
install -D -m 0644 riot-extras-desktop/extras/riot.hicolor.${N}x${N}.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done
install -D -m 0644 riot-extras-desktop/extras/riot.hicolor.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.png

