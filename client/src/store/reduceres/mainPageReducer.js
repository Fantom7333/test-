import { GET_COURSERS } from "../actions/actionTypes"




const initialState = {
    mainPageCourses: [
        
    ]
}



const mainPageReducer = ( state = initialState, action ) => {
    switch( action.type ) {

        case GET_COURSERS:
            return {
                ...state,
                mainPageCourses: action.courses
            }

        default:
            return state
    }
}

export default mainPageReducer