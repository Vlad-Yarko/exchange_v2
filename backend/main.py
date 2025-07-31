import asyncio

from src import api, bot


async def main():
    await asyncio.gather(
        # bot.run(),
        api.run()
    )


if __name__ == "__main__":
    asyncio.run(main())


# swagger_ui_oauth2_redirect_url: Annotated[
#             Optional[str],
#             Doc(
#                 """
#                 The OAuth2 redirect endpoint for the Swagger UI.

#                 By default it is `/docs/oauth2-redirect`.

#                 This is only used if you use OAuth2 (with the "Authorize" button)
#                 with Swagger UI.
#                 """
#             ),
#         ] = "/docs/oauth2-redirect",
#         swagger_ui_init_oauth: Annotated[
#             Optional[Dict[str, Any]],
#             Doc(
#                 """
#                 OAuth2 configuration for the Swagger UI, by default shown at `/docs`.

#                 Read more about the available configuration options in the
#                 [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
#                 """
#             ),
