from __future__ import annotations

from typing import Dict, List, Union

from ..helpers import parse_link_response, parse_user_response
from ..http_clients import AsyncClient
from ..types import (
    AdminUserAttributes,
    AuthMFAAdminDeleteFactorParams,
    AuthMFAAdminDeleteFactorResponse,
    AuthMFAAdminListFactorsParams,
    AuthMFAAdminListFactorsResponse,
    GenerateLinkParams,
    GenerateLinkResponse,
    Options,
    User,
    UserResponse,
)
from .gotrue_admin_mfa_api import AsyncGoTrueAdminMFAAPI
from .gotrue_base_api import AsyncGoTrueBaseAPI


class AsyncGoTrueAdminAPI(AsyncGoTrueBaseAPI):
    def __init__(
        self,
        *,
        url: str = "",
        headers: Dict[str, str] = {},
        http_client: Union[AsyncClient, None] = None,
    ) -> None:
        AsyncGoTrueBaseAPI.__init__(
            self,
            url=url,
            headers=headers,
            http_client=http_client,
        )
        self.mfa = AsyncGoTrueAdminMFAAPI()
        self.mfa.list_factors = self._list_factors
        self.mfa.delete_factor = self._delete_factor

    async def sign_out(self, jwt: str) -> None:
        """
        Removes a logged-in session.
        """
        return await self._request(
            "POST",
            "logout",
            jwt=jwt,
            no_resolve_json=True,
        )

    async def invite_user_by_email(
        self,
        email: str,
        options: Options = {},
    ) -> UserResponse:
        """
        Sends an invite link to an email address.
        """
        return await self._request(
            "POST",
            "invite",
            body={"email": email, "data": options.get("data")},
            redirect_to=options.get("redirect_to"),
            xform=parse_user_response,
        )

    async def generate_link(self, params: GenerateLinkParams) -> GenerateLinkResponse:
        """
        Generates email links and OTPs to be sent via a custom email provider.
        """
        return await self._request(
            "POST",
            "admin/generate_link",
            body={
                "type": params.get("type"),
                "email": params.get("email"),
                "password": params.get("password"),
                "new_email": params.get("new_email"),
                "data": params.get("options", {}).get("data"),
            },
            redirect_to=params.get("options", {}).get("redirect_to"),
            xform=parse_link_response,
        )

    # User Admin API

    async def create_user(self, attributes: AdminUserAttributes) -> UserResponse:
        """
        Creates a new user.

        This function should only be called on a server.
        Never expose your `service_role` key in the browser.
        """
        return await self._request(
            "POST",
            "admin/users",
            body=attributes,
            xform=parse_user_response,
        )

    async def list_users(self) -> List[User]:
        """
        Get a list of users.

        This function should only be called on a server.
        Never expose your `service_role` key in the browser.
        """
        return await self._request(
            "GET",
            "admin/users",
            xform=lambda data: [User.parse_obj(user) for user in data["users"]]
            if "users" in data
            else [],
        )

    async def get_user_by_id(self, uid: str) -> UserResponse:
        """
        Get user by id.

        This function should only be called on a server.
        Never expose your `service_role` key in the browser.
        """
        return await self._request(
            "GET",
            f"admin/users/{uid}",
            xform=parse_user_response,
        )

    async def update_user_by_id(
        self,
        uid: str,
        attributes: AdminUserAttributes,
    ) -> UserResponse:
        """
        Updates the user data.

        This function should only be called on a server.
        Never expose your `service_role` key in the browser.
        """
        return await self._request(
            "PUT",
            f"admin/users/{uid}",
            body=attributes,
            xform=parse_user_response,
        )

    async def delete_user(self, id: str) -> None:
        """
        Delete a user. Requires a `service_role` key.

        This function should only be called on a server.
        Never expose your `service_role` key in the browser.
        """
        return await self._request("DELETE", f"admin/users/{id}")

    async def _list_factors(
        self,
        params: AuthMFAAdminListFactorsParams,
    ) -> AuthMFAAdminListFactorsResponse:
        return await self._request(
            "GET",
            f"admin/users/{params.get('user_id')}/factors",
            xform=AuthMFAAdminListFactorsResponse.parse_obj,
        )

    async def _delete_factor(
        self,
        params: AuthMFAAdminDeleteFactorParams,
    ) -> AuthMFAAdminDeleteFactorResponse:
        return await self._request(
            "DELETE",
            f"admin/users/{params.get('user_id')}/factors/{params.get('factor_id')}",
            xform=AuthMFAAdminDeleteFactorResponse.parse_obj,
        )
