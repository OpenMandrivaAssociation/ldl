%define NAME	LDL
%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		ldl
Version:	2.1.0
Release:	3
Epoch:		1
Summary:	Routines for performing LDL' factorization of sparse matricies
Group:		System/Libraries
License:	LGPLv2+
URL:		https://www.cise.ufl.edu/research/sparse/ldl/
Source0:	http://www.cise.ufl.edu/research/sparse/ldl/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
LDL provides routines for performin LDL' factorization of sparse matricies.

%package -n %{libname}
Summary:	Library of routines for performing LDL' factorization of sparse matricies
Group:		System/Libraries
%define	oldname	%{mklibname %{name} 2.1.0}
%rename		%{oldname}

%description -n %{libname}
LDL provides routines for performin LDL' factorization of sparse matricies.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for performing LDL' factorization of sparse matricies
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
LDL provides routines for performin LDL' factorization of sparse matricies.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make -f Makefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} *.o
popd

%install
cd %{NAME}

for f in Lib/*.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
