from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status, serializers
from rest_framework.exceptions import Throttled


class DreamerValidationError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")

    def __init__(
            self, message, message_code, detail=None, code=None, data=None, is_error=True
    ):
        self.message_code = message_code
        self.message = message
        self.status = "error" if is_error else "success"
        self.data = data
        super(DreamerValidationError, self).__init__(detail=detail, code=code)


def humanize_dict_exception(exception_detail, key, message):
    if isinstance(exception_detail, list):
        error_result = ""
        for error_detail in exception_detail:
            if isinstance(error_detail, dict):
                for _key in error_detail:
                    exception = humanize_dict_exception(
                        error_detail[_key], key, message
                    )
                    message += exception
                return message
            if hasattr(error_detail, "code") and error_detail.code in [
                "required",
                "null",
                "blank",
            ]:
                error_result += f'{_("Please Enter")} {_(key)}'
            elif hasattr(error_detail, "code") and error_detail.code in [
                "invalid",
                "invalid_choice",
                "does_not_exist",
            ]:
                error_result += f'{_("Please enter")} {_(key)} {_("correctly")}'
            else:
                error_result += f"{_(key)} {error_detail}"

        return error_result
    if isinstance(exception_detail, dict):
        for key in exception_detail:
            exception = humanize_dict_exception(exception_detail[key], key, message)
            message += exception
        return message
    # should not reach here
    return _("Something went wrong")


def humanize_exception(exc):
    message = ""
    for key in exc.detail:
        exception_detail = exc.detail[key]
        if isinstance(exception_detail, (list, dict)):
            message += humanize_dict_exception(exception_detail, key, "")
        else:
            message += exception_detail
        message += " "
    return message


def dreamer_exception_handler(exc, context):
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)

    if response is not None:
        data = {"errors": response.data}
        response.data = data
        if isinstance(exc, Http404):
            response.data["message_code"] = "not_found"
            exception_message = str(exc).lower()
            if "matches the given query" in exception_message:

                response.data[
                    "message"
                ] = f"{exception_message.replace('matches the given query', '').replace('no ', '').strip()} {_('was not found')}"

            else:
                response.data["message"] = str(exc)
        if isinstance(exc, DreamerValidationError):
            response.data["message_code"] = exc.message_code
            response.data["message"] = exc.message
            response.data["data"] = exc.data
            response.data["status"] = exc.status

        if isinstance(exc, serializers.ValidationError):
            response.data["message"] = humanize_exception(exc)
            response.data["message_code"] = "unknown"
        # response.data['code'] = exc.code
        if isinstance(exc, Throttled):
            response.data["message"] = _("You have reached your request limit")
            time = list(filter(lambda i: i.isdigit(), exc.detail.split()))
            if time:
                time = time[0]
                response.data[
                    "message"
                ] = f"{_('You have reached your request limit please try in')} {time} {_('second')}"
            response.data["message_code"] = "unknown"
        if "status" not in response.data:
            response.data["status"] = "error"
    return response
