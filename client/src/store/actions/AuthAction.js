import { LOGIN_USER, LOGOUT_USER, LOG_ERROR_MASSAGE } from "./actionTypes"
import axios from "axios"


////////////    2 ajax requests post & get   name:   password: 

export const authDataPost = ( data, ownProps ) => {
    return async (dispatch, getState )=> {
        await axios.post("http://127.0.0.1:5000/authorization/log_in", data )
            .then( res => {
                if( res.data.error ) {
                    dispatch( logErrorMassage() )
                } else if ( !res.data.error ) {
                    dispatch( loginUser() )
                    ownProps.history.push("/")
                    
                }
            })
            .catch(function (error) {
                console.log(error);
              });
    }
}

const logErrorMassage = () => {
    return {
        type: LOG_ERROR_MASSAGE,
    }
}

export const loginUser = () => {
    return {
        type: LOGIN_USER
    }
}

export const logoutUser = () => {
    return {
        type: LOGOUT_USER
    }
}