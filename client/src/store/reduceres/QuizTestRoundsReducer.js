import {ADD_QUIZ_ANSWERS, DELETE_ALL_ANSWERS , DECREMENT_CURRENT_QUIZ, INCREMENT_CURRENT_QUIZ, CLEAR_QUIZ_ANSWERS} from "../actions/actionTypes"

const initialState = {
    current: 0,
    quizAsnwers: [
        // { isAnswer: true,   answer: "5 + 5",  rightOption: 1,  options: [{ aswer1: 10 }, { aswer2: 2 }, {aswer3: 1 }, {aswer3: 322 }] },
        // { isAnswer: false,  theoryName: "Градиентный спуск", theory: "Градиентный спуск" } ,
        // { isAnswer: true,   answer: "10 + 5",  rightOption: 3,  options: [{ aswer1: 10 }, { aswer2: 2 }, {aswer3: 15 }, {aswer3: 8 }]  },
    ]
}


const QuizTestRoundsReducer = ( state = initialState , action ) => {
    switch( action.type ) {


        case DECREMENT_CURRENT_QUIZ:
            return {
                ...state,
                current: state.current - 1
            }  
        case INCREMENT_CURRENT_QUIZ:
            return {
                ...state,
                current: state.current + 1
            }

          


        case ADD_QUIZ_ANSWERS:
            return {
                ...state,
                quizAsnwers: [...action.answers ]
            }
          
        // case DELETE_ALL_ANSWERS:
        //     return {
        //         ...state,
        //         quizAsnwers: []
        //     }    

        case CLEAR_QUIZ_ANSWERS:
            return {
                ...state,
                quizAsnwers: [],
                current: 0
            }    
        default:
            return state
    }
}


export default QuizTestRoundsReducer