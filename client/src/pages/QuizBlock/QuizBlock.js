import React from 'react'
import { connect } from 'react-redux'
import { withRouter } from "react-router-dom"

import QuizTest from "../../components/QuizTest/QuizTest"

import classes from "./QuizBlock.module.css"
import NavBar from '../../components/UI/NavBar/NavBar'

function QuizBlock(props) {


    const quizPath = +props.location.pathname.split("/")[2]

    
    // console.log("fd",  )

    // console.log("Props",  props.match.params.id )

    return (
        <div className = { classes.QuizBlock }>

        
       {/* <div className = { classes.QuizBlock_wrapper }>
            <h1>{ props.quiz[quizPath].courseBlocks[props.match.params.id].blokName }</h1>

                <QuizTest blockId = {props.match.params.id} pathToBack = { quizPath } />
          </div> */ }   <NavBar />
          
            
        </div>
    )
}

function mapStateToProps( state ) {

    return {
        quiz: state.quizReducer.quiz,
    }

}

function mapDispatchToProps( dispatch ) {
    return {
        
    }
}



export default connect( mapStateToProps, mapDispatchToProps ) ( withRouter(QuizBlock) )



