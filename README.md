Welcome to DWM Django Rest Framework Boilerplate!
===================

[![Build Status](https://travis-ci.org/jaarce/drf_boilerplate.svg)](https://travis-ci.org/jaarce/drf_boilerplate)

[![](http://www.directworksmedia.com/static/images/logo-light.png)](http://www.directworksmedia.com/)

----------


<i class="icon-file"></i> userprofile.views
-------------

>#### userprofile.views.ManualLogin
> ----------
> **endpoint: /v1/login/form/**
> **method: POST**
> **namespace: login-form**
>
>  Endpoint for manual User Login via username and password.
>  :param request
>  :return Response():

----------

>#### userprofile.views.ManualRegister
> ----------
> **endpoint: /v1/registration/form/**
> **method: POST**
> **namespace: registration-form**
>
>  Endpoint for manual registration via email & password
>  :param request:
>  :return Response():

----------
>#### userprofile.views.ManualRegister
> ----------
> **endpoint: /v1/registration/check/**
> **method: POST**
> **namespace: registration-check**
>
>  Endpoint for checking if username exists
>  :param request:
>  :return Response():

----------
>#### userprofile.views.SocialMediaConnectViewSet
> ----------
> **endpoint: /v1/social-media/check_social_id/**
> **method: POST**
> **namespace: social_media-check-social-id**
>
>  Endpoint for checking social ID password
>  :param request:
>  :return Response():

----------

>#### userprofile.views.SocialMediaConnectViewSet
> ----------
> **endpoint: /v1/social-media/check_username/**
> **method: POST**
> **namespace: social_media-check-username**
>
>  Endpoint for checking username
>  :param request:
>  :return Response():

----------

>#### userprofile.views.SocialMediaConnectViewSet
> ----------
> **endpoint: /v1/social-media/connect/**
> **method: POST**
> **namespace: social_media-connect**
>
>  Endpoint for connecting to social media
>  :param request:
>  :return Response():
