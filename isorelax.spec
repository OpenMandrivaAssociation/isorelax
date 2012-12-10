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
%define gcj_support	1

Name:           isorelax
Summary:        Public interfaces for RELAX Core
Url:            http://iso-relax.sourceforge.net/
Version:        0.1
Release:        %mkrel 2
License:        MIT
Group:          Development/Java
%if %{gcj_support} 	 
BuildRequires:	java-gcj-compat-devel 	 
%else 	 
BuildArch:	noarch 	 
BuildRequires:	java-devel
%endif

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
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr apidocs/* %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%if %{gcj_support} 	 
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}


%changelog
* Tue Apr 26 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.1-2mdv2011.0
+ Revision: 659415
- Revert to build with gcj support and do not install versioned doc dir

* Mon Apr 25 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.1-1
+ Revision: 659069
- Update and rebuild

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

  + Jérôme Soyer <saispo@mandriva.org>
    - Bump Release

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 1:0-0.1.release20050331.1.2.4mdv2009.0
+ Revision: 140792
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 1:0-0.1.release20050331.1.2.4mdv2008.1
+ Revision: 120896
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:0-0.1.release20050331.1.2.3mdv2008.0
+ Revision: 87393
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 1:0-0.1.release20050331.1.2.2mdv2008.0
+ Revision: 53182
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)

* Tue Jul 03 2007 David Walluck <walluck@mandriva.org> 1:0-0.1.release20050331.1.2.1mdv2008.0
+ Revision: 47371
- gcj support
- Import isorelax



* Tue Mar 06 2007 Vivek Lakshmanan <vivekl@redhat.com> 1:0-0.1.release20050331.1jpp.2.fc7
- Rebuild

* Tue Mar 06 2007 Vivek Lakshmanan <vivekl@redhat.com> 1:0-0.1.release20050331.1jpp.1.fc7
- First Fedora build

* Mon Feb 12 2007 Andrew Overholt <overholt@redhat.com> 1:0-0.1.release20050331.1jpp.1
- Clean up
- Remove tests
- Fix e:nvr for new scheme (0.Z.tag.Xjpp.Y%%{?dist}) and bump epoch for
  upgrades
- Add instructions for how to create source drop
- Don't do javadoc symlinking in %%post{,un}
- Remove Obsoletes and Provides on isorelax-bootstrap as they were never
  shipped in Fedora and I don't know what version to Obsolete/Provide

* Wed Mar 22 2006 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20041111.2jpp
- By default omit tests requiring xercesjarv
- Add postun for javadoc
- Drop useless macros for name, version, etc.

* Tue Aug 23 2005 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20041111.1jpp
- Upgrade to 20041111

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1-0.20030108.3jpp
- Rebuild with standard version scheme

* Wed Aug 25 2004 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20030108.2jpp
- Build with ant-1.6.2

* Tue Jul 06 2004 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20030108.1jpp
- First build from sources into free section
- Use xercesjarv instead of swift as verifier impl
