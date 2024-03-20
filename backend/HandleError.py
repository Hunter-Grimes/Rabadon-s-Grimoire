def riotApiError(errCode):
    match errCode:
        case 400:
            raise Exception("Riot API: Bad Request")
        case 401:
            raise Exception("Riot API: Unauthorized")
        case 403:
            raise Exception("Riot API: Forbidden")
        case 404:
            raise Exception("Riot API: Data Not Found")
        case 405:
            raise Exception("Riot API: Method Not Allowed")
        case 415:
            raise Exception("Riot API: Unsupported Media Type")
        case 429:
            raise Exception("Riot API: Rate Limit Exceeded")
        case 500:
            raise Exception("Riot API: Internal Server Error")
        case 502:
            raise Exception("Riot API: Bad Gateway")
        case 503:
            raise Exception("Riot API: Service Unavailable")
        case 504:
            raise Exception("Riot API: Gateway Timeout")