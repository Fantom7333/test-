// {
// 	"login": "testUser",
// 	"email": "testEmail@xuz.ru",
// 	"password": "322322"
// }

import axios from "axios"
import { EMAIL_ERROR, NAME_ERROR, REGISTER_ERROR } from "./actionTypes"
import { loginUser } from "./AuthAction"


export const postRegisterData = ( data, props ) => {
    return async dispatch => {
        await axios.post("http://localhost:5000/authorization/sign_up", data )
            .then( res => {
                if ( res.data.error ) {
                    dispatch( registerError(true) )
                } else {
                    dispatch( loginUser() )
                    props.history.push("/")
                }
            })
    }
}

export const registerError = errorType => {
    return {
        type: REGISTER_ERROR,
        errorType
    }
}

const emailError = () => {
    return {
        type: EMAIL_ERROR
    }
}

const nameError = () => {
    return {
        type: NAME_ERROR
    }
}