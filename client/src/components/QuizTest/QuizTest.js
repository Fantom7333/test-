import React, { useState, useEffect } from 'react'

import classes from "./QuizTest.module.css"
import { NavLink } from "react-router-dom"

import QuizTestRounds from "../QuizTestRounds/QuizTestRounds"
import { connect } from 'react-redux'


import QuizBlockOption from "../../components/QuizBlockOption/QuizBlockOption"

import Button from '@material-ui/core/Button';


import { addQuizAnswers, incrementCurrentQuiz, decrementCurrentQuiz, clearQuizAnswers } from "../../store/actions/QuizTestRoundsAction"


class QuizTest extends React.Component  {
    
    // console.log("Test", this.props.quiz[this.props.pathToBack].courseBlocks[this.props.blockId].blockAswersAndTheory )

    
    componentDidMount() {
        // if( this.props.quizAsnwers.quizAsnwers.length <= 0) {
        //     this.props.addQuizAnswers(this.props.quiz[this.props.pathToBack].courseBlocks[this.props.blockId].blockAswersAndTheory)
        // }
        this.props.addQuizAnswers( this.props.blockId )
    }
    
    componentWillUnmount() {
        this.props.clearQuizAnswers()
    }



    

    // console.log( "Кунри", this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current ])
    renderContent = () => {
        if( this.props.quizAsnwers.quizAsnwers.length > 0) {
            let data = this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current ]
                if ( data.isAnswer === true ) {
                    return (
                        <React.Fragment>
                            <h1>{ data.answer }</h1>
                            
                        </React.Fragment>
                    )
                } else {
                    return (
                        <React.Fragment>
                            <h1>{ data.theoryName }</h1>
                            <p>{ data.theory }</p>
                        </React.Fragment>
                    )
                }
        }
        return null
            
    }


    onIncreaseHandler = () => {
        if ( this.props.quizAsnwers.current < this.props.quizAsnwers.quizAsnwers.length - 1 ) {
            this.props.incrementCurrentQuiz()
        }
    }

    onDecreaseHandler = () => {
        if ( this.props.quizAsnwers.current > 0 ) {
            this.props.decrementCurrentQuiz()
        }
    }


    optionClickHandler = (id, rightAnswer) => {
        if ( id + 1 === rightAnswer ) {
            alert("It's right")
        } else {
            alert("fleire")
        }
        
    }


    renderOptions () {
        let data = this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current]
        // const rightAnswer = this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current].rightOption
        console.log( this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current] )
        if(  this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current] != undefined && this.props.quizAsnwers.quizAsnwers[ this.props.quizAsnwers.current].isAnswer) {
            return data.options.map( (item, index ) => {
                return (
                    <React.Fragment key = { index }>
                        <button onClick = { () => this.optionClickHandler(index, data.rightOption) } style = {{display: "block", background: "none", border: "none", outline: "none"}}>
                            <QuizBlockOption option = { item.option } />
                        </button>
                    </React.Fragment>
                )
            })
            console.log("DADA", data )
        }
        
        
        
    }



    render(){
        // console.log( this.props.quizAsnwers.quizAsnwers.map( (item) => console.log( item.answer ) ) )
        document.title = "Дарвоа"


        // const way = this.props.quiz[this.props.pathToBack].courseBlocks[this.props.blockId].blockAswersAndTheory
        const way = this.props.quizAsnwers
        let rounds = []


        
        function quizRoundsRender() {
            for ( let i = 0; i <  way.length; i++) {
              rounds.push (
                <React.Fragment key = { i }>
                    <QuizTestRounds symbol = { way[i].isAnswer ? "?" : "=>"} />
                </React.Fragment>
              )            
            }
        }
        quizRoundsRender()



        


        return (
            <div className = { classes.QuizTest }>
                <NavLink className = { classes.QuizTest_exit } to = { "/quizes/" + this.props.pathToBack }>
                    <i className ="far fa-times-circle"></i>
                </NavLink>
    
    
    
                <div className = { classes.QuizTest_rounds}>
                    { rounds }                
                </div>
    
                <div>
                    { this.renderContent() }
                </div>
    
            <div className = { classes.QuizTest_controls}>
    
                <Button style = {{ visibility: this.props.quizAsnwers.current === 0 ? "hidden" : "visible"}} onClick = { () =>  this.onDecreaseHandler() } variant="contained" color="primary" className={classes.margin}>Pre</Button>
                <Button style = {{ visibility: this.props.quizAsnwers.current === this.props.quizAsnwers.quizAsnwers.length - 1 ? "hidden" : "visible"}} onClick = { () =>  this.onIncreaseHandler() } variant="contained" color="primary" className={classes.margin}>next</Button>
            </div>
            
            { this.renderOptions() }
            
            </div>
        )
    }
    






}


function mapStateTothisProps ( state ) {

    return {
        quiz: state.quizReducer.quiz,
        quizAsnwers: state.QuizTestRoundsReducer
    }
}


function mapDispatchTothisProps ( dispatch ) {
    return {
        addQuizAnswers: answers => dispatch( addQuizAnswers(answers) ),
        incrementCurrentQuiz: () => dispatch( incrementCurrentQuiz() ),
        decrementCurrentQuiz: () => dispatch( decrementCurrentQuiz() ),
        clearQuizAnswers: () => dispatch(clearQuizAnswers() )
    }
}



export default connect( mapStateTothisProps, mapDispatchTothisProps ) ( QuizTest )
