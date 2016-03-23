# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Lib.TornadoExtend import HttpResponseCode
from Model.MemberAdvice import MemberAdvice
from Controller.Main.BaseProcess import BaseProcess
from Model.Version import Version

class PersonCenter(BaseProcess):

    def get_version_update(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        version = params.get('version', None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        current_version = Version.get_latest_version()
        if current_version.version == version:
            return self.on_response_success(dict(version=current_version.version))

        return self.on_response_success(dict(version=current_version.version,url=current_version.url))

    def get_user_agreement(self):
        params = self.get_params()
        access_token = params.get('access_token', None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        ret = dict(html='Common/Agreement.html',params='')
        return ret

    def commit_advice(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        content = params.get('content', None)
        contactinformation = params.get('contactinformation',None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        advice = MemberAdvice()
        advice.content = content
        advice.contactinformation = contactinformation
        advice.member_id = member.id
        advice.save()

        return self.on_response_success()
