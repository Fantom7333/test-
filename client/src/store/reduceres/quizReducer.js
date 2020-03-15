import { ADD_NEW_BLOCKS, CLEAR_COURSES } from "../actions/actionTypes"



const initialState = {
    currentCourse: [],
    quiz: [
        // {
        //     id: 0,
        //     name: "Высшая математикаf sa fasdfs",  
        //     img: "",
        //     courseInfo: "Это курс по высшей математики",
        //     courseBlocks: [
    
        //         {   blokName: "Деф уравнения",
        //             // blockAswersAndTheory: [
        //             //     { isAnswer: true,   answer: "5 + 5",  rightOption: 1,  options: [{ aswer1: 10 }, { aswer2: 2 }, {aswer3: 1 }, {aswer3: 322 }] },
        //             //     { isAnswer: false,  theoryName: "Градиентный спуск", theory: testTheory } ,
        //             //     { isAnswer: true,   answer: "10 + 5",  rightOption: 3,  options: [{ aswer1: 10 }, { aswer2: 2 }, {aswer3: 15 }, {aswer3: 8 }]  },
        //             // ]
        //         }]
        //     },
            
        
    ]
}




export default function quizReducer( state = initialState, action ) {
    switch( action.type ) {
         case ADD_NEW_BLOCKS:
             return {
                 ...state,
                 quiz: action.data
             }

        case CLEAR_COURSES: 
            return {
                ...state,
                quiz: []
            }     
        default:
            return state
    }
}