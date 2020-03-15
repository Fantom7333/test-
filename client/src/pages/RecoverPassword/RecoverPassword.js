import React from 'react'

import classes from "./RecoverPassword.module.css"
import NavBar from "../../components/UI/NavBar/NavBar"


import {  withRouter  } from "react-router-dom"

// import { useHistory } from 'react-router-dom';
import { connect } from 'react-redux';




function RecoverPassword(props) {



    const onSubmitHandler = (event) => {
        event.preventDefault()
        
        props.history.push('/authorization/confirm_new_password')

    }


        const InputName = React.createRef()




        return (
            <div className = { classes.Authentication }>
                <NavBar />
                <h1>Востановление паролья</h1>
                
            <div className = { classes.Authentication_wrapper }>
                
                    
                    <form className = { classes.Authentication_form } onSubmit = { event => onSubmitHandler(event) }>

                        
                        <input id = "forgot" type = "email" className = { classes.Authentication_input } ref = { InputName } required minLength = "6" maxLength = "25" /> 
                        <label htmlFor = "forgot">Введите email</label>

                        <input  type = "submit" className = { classes.Authentication_input } value = "Отправить мне код"  />
                        
                         
                    </form>

                    

                    
                </div>
                
                
            </div>
        )
}


function mapStateToProps( state ) {
    return {
    }
}
function mapDispatchToProps( dispatch  ) {
    return {

    }
}


export default connect(mapStateToProps, mapDispatchToProps) (withRouter(RecoverPassword)) 