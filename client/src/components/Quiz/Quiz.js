// home


import React from 'react'

import { NavLink } from "react-router-dom"

import classes from "./Quiz.module.css"
import { connect } from 'react-redux'

import { getCourses } from "../../store/actions/mainPageAction"

class Quiz extends React.Component {

    state = {
        loading: true
    }
 

    componentDidMount() {
        this.props.getCourses()
        this.setState({
            loading: false
        })
    }
    

    render() {
        document.title = "Наши курсы";


    const renderQuizes =  this.props.mainPageQuizes.map( (item, index ) => {

        return (
            <div key = { item + index } className = { classes.Quiz_item }>
                <NavLink to = { `/${item.course_name}` }>
                    
                    <img src = { item.avatar } />
                    <h6> { item.course_name }</h6>
                </NavLink>
            </div>
        
        )
        
    })


    const content = (
        <React.Fragment>
            <h1>Наши курсы</h1>
        
            <div className = { classes.Quiz_wrapper }>
                
                { renderQuizes }
                
            </div>
        </React.Fragment>
    )

    const renderContent = this.state.loading ? <h1>loading...</h1> : content

        return (    
            <div className = { classes.Quiz }>
                { renderContent }
            </div>        
        )
    }
    
}


function mapStateToProps( state ) {

    return {
        quiz: state.quizReducer.quiz,
        mainPageQuizes: state.mainPageReducer.mainPageCourses
    }

}

function mapDispatchToProps(dispatch) {
    return {
        getCourses: (id) => dispatch( getCourses(id) )
    }
}



export default connect( mapStateToProps, mapDispatchToProps ) ( Quiz )
