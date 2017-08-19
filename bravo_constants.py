
class Errors:
    success = 0;

    # common json pattern must be:
    # {code:int, data:{}, msg:string}
    system_json_pattern = 306;
    # network error
    system_network_http_get = 307;
    system_network_json_parse = 308;
    system_network_http_post = 309;

    @staticmethod
    def is_success(current_code):
        return current_code == Errors.success;

    @staticmethod
    def valid_msg(msg):
        # @see: Errors.system_json_pattern
        return "code" in msg and "data" in msg;