import React, { Component } from 'react'

import classes from "./ConfirmChangePassword.module.css"
import NavBar from "../../components/UI/NavBar/NavBar"


import {  withRouter, NavLink  } from "react-router-dom"

// import { useHistory } from 'react-router-dom';
import { connect } from 'react-redux';




function ConfirmChangePassword(props) {



    const onSubmitHandler = (event) => {
        event.preventDefault()
        
        props.history.push('/')

    }


        const InputName = React.createRef()




        return (
            <div className = { classes.Authentication }>
                <NavBar />
                <h1>Ввод кода подтверждения и нового пароля</h1>
                
            <div className = { classes.Authentication_wrapper }>
                
                    
                    <form className = { classes.Authentication_form } onSubmit = { event => onSubmitHandler(event) }>

                        
                        <input id = "forgot" type = "password" className = { classes.Authentication_input } ref = { InputName } required minLength = "6" maxLength = "20" /> 
                        <label htmlFor = "forgot">Новый пароль</label>

                        <input id = "forgot" type = "text" className = { classes.Authentication_input } ref = { InputName } required minLength = "10" maxLength = "10" /> 
                        <label htmlFor = "forgot">Код подтверждения</label>

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


export default connect(mapStateToProps, mapDispatchToProps) (withRouter(ConfirmChangePassword)) 