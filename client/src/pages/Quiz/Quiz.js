import React from 'react'

import { NavLink,  withRouter, Link } from "react-router-dom"
import { connect } from "react-redux"

import classes from "./Quiz.module.css"
import NavBar from '../../components/UI/NavBar/NavBar'

import { getDataFromQuizes, clearBlock } from "../../store/actions/quizAction"




class Quiz extends React.Component {

    
    // props.quiz[ props.match.params.id ]

    state = {
        loading: true
    }

    
    componentDidMount() {
        this.props.getDataFromQuizes(this.props.match.params.course)

        this.setState({
            loading: false
        })
        
    }
    
    componentWillUnmount() {
        // this.props.clearBlock()
        // this.props.getDataFromQuizes(this.props.match.params.course)
    }


    
    
//     <NavLink to = { `/quizes/${props.match.params.id}/${index }` }>
//     { item.blokName }
// </NavLink>

// <Link to = { `/quizes/${props.match.params.id}/${index }` }>
//                     { item.blokName }
//                     </Link>



// <NavLink to = { `${props.match.url}/block/${index }` }>
//                     { item.blokName }
//                     </NavLink>



    blocksRender = ( blockQuiz ) => {
        return blockQuiz.map( (item, index) => {
            let mapingLinks = []
            
            if ( this.props.isAuth ) {
                mapingLinks.push(
                    <NavLink to = { `${this.props.match.url}/${ index }` }>
                        { item.section_name_display }
                    </NavLink>  
                ) 
            } else {
                mapingLinks.push(
                    <NavLink to = "/authorization/log_in" >
                        { item.section_name_display }
                    </NavLink> 
                )
                  
            }
            
            return (
                <div className = { classes.courseBlocks_round } key = { item + index} >

                    { mapingLinks }                
                </div>
            )
        })
    }

    // console.log( props.quiz[ props.match.params.id ]  )


    // { this.blocksRender( this.props.quiz ) }
    render() {
        console.log( this.props.quiz )
        // console.log( this.props.match.params.course )
        // console.log("PSO", this.props.blockId )
        // console.log("QUIZ", this.props.quiz )
        // console.log("Blocks", this.props.quiz )
        // console.log("ID", this.props.match.params.id)

        const paramsQuiz = ( quiz ) => {
            return (
                <div className = { classes.Quiz_wrapper_info } >
                    <h1>Курс { this.props.match.params.course }</h1>
    
                   {/*  <img src = { quiz.avatar } />*/} 
    
                    
                    {/* <p>{ quiz.section_name_display } </p> */}
                </div>
                    
            )
        }


        const renderContent = (
            
            <React.Fragment>
                <div className = { classes.Quiz_wrapper }>
                    { paramsQuiz( this.props.quiz[0] ) }

                    { this.blocksRender( this.props.quiz ) }
                </div>
                
            </React.Fragment>
            

        
        )



        const content = this.state.loading ? <h1>loading...</h1> : renderContent

        return (
            <div className = { classes.Quiz }>
                <NavBar />

                
                { content }
            </div>
        )
    }
    
}




function mapStateToProps( state ) {

    console.log( state )
    return {
        quiz: state.quizReducer.quiz,
        isAuth: state.AuthReducer.isAuth
        // currentCourse: state.quizReducer.currentCourse
    }

}

function mapDispatchToProps(dispatch) {
    return {
        getDataFromQuizes: id => dispatch( getDataFromQuizes(id) ),
        clearBlock: () => dispatch( clearBlock() )
    }
}


export default connect( mapStateToProps, mapDispatchToProps ) ( withRouter(Quiz) )
