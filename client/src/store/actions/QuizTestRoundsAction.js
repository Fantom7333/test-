import {ADD_QUIZ_ANSWERS, DELETE_ALL_ANSWERS, INCREMENT_CURRENT_QUIZ, DECREMENT_CURRENT_QUIZ, CLEAR_QUIZ_ANSWERS} from "./actionTypes"
import axios from "axios"


let newAnswers = [
//  {
    // id: 1,
    // blokName: "Деф уравнения",
    // blockAswersAndTheory: [
        { isAnswer: true,   answer: "5 + 5",  rightOption: 1,  options: [{ option: 10 }, { option: 2 }, {option: 1 }, {option: 322 }] },
        { isAnswer: false,  theoryName: "Градиентный спуск", theory: "Градиентный спуск" },
        { isAnswer: true,   answer: "10 + 5",  rightOption: 3,  options: [{ option: 10 }, { option: 2 }, {option: 15 }, {option: 8 }]  },
    // ]
//  }
]
    


export const addQuizAnswers = ( id ) => {
    return async dispatch => {
        dispatch( addDataToState(newAnswers) )
        try {
            const response = await axios.get(`/quizes/:id/block/${id}`)
        // const answers = response.data
        const answers = response.data
        
        } catch (error) {
            console.error("QUIZ TEST ACTION GET", error)
        }
        
    }
    
}


const addDataToState = (answers) => {
    return {
        type: ADD_QUIZ_ANSWERS,
        answers
    }
}


export const incrementCurrentQuiz = () => {
    return {
        type: INCREMENT_CURRENT_QUIZ,
    }
}

export const decrementCurrentQuiz = () => {
    return {
        type: DECREMENT_CURRENT_QUIZ,
    }
}

export const clearQuizAnswers = () => {
    return {
        type: CLEAR_QUIZ_ANSWERS
    }
}