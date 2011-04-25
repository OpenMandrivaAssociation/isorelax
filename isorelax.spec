# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define cvstag  release-20050331

Name:           isorelax
Summary:        Public interfaces for RELAX Core
Url:            http://iso-relax.sourceforge.net/
Version:        0.1
Release:        %mkrel 1
License:        MIT
Group:          Development/Java
BuildRequires:  java-devel
BuildArch:      noarch

# mkdir isorelax-release-20050331-src
# cd isorelax-release-20050331-src
# cvs -d:pserver:anonymous@iso-relax.cvs.sourceforge.net:/cvsroot/iso-relax \
#   export -r release-20050331 src lib
# cvs -d:pserver:anonymous@iso-relax.cvs.sourceforge.net:/cvsroot/iso-relax \
#   co -r release-20050331 build.xml
# rm -rf CVS
# cd ..
# tar cjf isorelax-release-20050331-src.tar.bz2 isorelax-release-20050331-src
Source0:        %{name}-%{cvstag}-src.tar.bz2
Patch0:         %{name}-apidocsandcompressedjar.patch

BuildRequires:  java-devel
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
Requires:       xerces-j2
Requires:       xml-commons-jaxp-1.3-apis
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The ISO RELAX project was started to host public interfaces
useful for applications to support RELAX Core. Now, however,
some of the hosted material is schema language-neutral.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{cvstag}-src
find . -name "*.jar" -exec rm -f {} \;
ln -s %{_javadir}/ant.jar lib/
%patch0 -p0

%build
export CLASSPATH=$(build-classpath \
xerces-j2 \
xml-commons-jaxp-1.3-apis \
)
%{ant} release

%install
rm -rf %{buildroot}
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && \
 for jar in *-%{version}*; do \
     ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; \
 done
)

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*
