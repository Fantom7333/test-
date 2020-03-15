import React, { Component, useState } from 'react'
import { NavLink, withRouter } from "react-router-dom"
import axios from "axios"
 import NavBar from "../../components/UI/NavBar/NavBar"

import classes from "./Registration.module.css"
import { connect } from 'react-redux'

import { postRegisterData, registerError } from "../../store/actions/RegistrationAction"


function Registration( props ) {

    const [logPasswordRepeadError, setPasswordRepeadError] =  useState()

    const inputName = React.createRef()
    const inputEmail = React.createRef()
    const inputPassword = React.createRef()
    const inputRepeatPassword = React.createRef()



    let state = []



    const onSubmitHandler = event => {
        event.preventDefault()
        if( inputPassword.current.value.trim() === inputRepeatPassword.current.value.trim() ) {
            props.postRegisterData( {
                    login: inputName.current.value,
                    email: inputEmail.current.value,
                    password: inputPassword.current.value 
                }, props )
            // return props.history.push('/')
        } else {
            props.registerError( false )
            setPasswordRepeadError("Пароли не совпадают")
        }

        
    }

    // const getRegisterData = () => {
    //     axios.get("http://localhost:3000/registration")
    //         .then( res => {
    //             console.log( res )
    //         })
    // }

 



    return (
        <div className = { classes.Registration}>
            <NavBar />
            <h1>Регистрация</h1>

            <div className = { classes.Registration_wrapper }>
                
                <form onSubmit = { event => onSubmitHandler(event) } className = { classes.Registration_wrapper_form }>

                <p style = {{color: "red"}}>{ props.isError ? "Такой пользователь или email уже есть в системе"  : logPasswordRepeadError } </p>


                    <input id = "name" type = "name" placeholder = "имя" ref = { inputName } required minLength = "6" maxLength = "15" />
                    <label htmlFor = "name">Имя</label>

                    <input id = "email" type = "email" placeholder = "email" ref = { inputEmail } required minLength = "6" maxLength = "25" />
                    <label htmlFor = "email">email</label>

                    <input id = "password" type = "password" placeholder = "пароль" ref = { inputPassword } required minLength = "6" maxLength = "20" />
                    <label htmlFor = "password">пароль</label>

                    <input id = "passwordAgain" type = "password" placeholder = "и еще раз пароль" ref = { inputRepeatPassword } required minLength = "6" maxLength = "20" />
                    <label htmlFor = "passwordAgain">и еще раз пароль</label>

                    <input type = "submit" value = "Зарегистрироваться" />



                    <NavLink to = "/authorization/log_in">войти</NavLink>
                </form>

            </div>

        </div>
    )
}




function mapStateToProps( state ) {
    return {
        isError: state.RegistrationReducer.isError
    }
}
function mapDispatchToProps( dispatch ) {
    return {
        postRegisterData: (data, props) => dispatch( postRegisterData( data, props )),
        registerError: typeError => dispatch( registerError( typeError )) 
    }
}



export default connect( mapStateToProps, mapDispatchToProps) ( withRouter(Registration) )