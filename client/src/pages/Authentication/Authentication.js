import React, { Component, useState } from 'react'

import classes from "./Authentication.module.css"
import NavBar from "../../components/UI/NavBar/NavBar"


import { NavLink, withRouter  } from "react-router-dom"

// import { useHistory } from 'react-router-dom';
import { connect } from 'react-redux';

import {authDataPost}  from "../../store/actions/AuthAction"

import is from "is_js"



function Authentication(props) {

    const [ isAuthDataRight, setAuthData ] = useState("неверный пароль или имя" )

    // let state = {
    //     data: {name: "Roland", password: 123}
    // }

    


    console.log(props.history)

    const onSubmitHandler = (event) => {
        event.preventDefault()

        const name = InputName.current.value
        const password = InputNaPassword.current.value

        if( name.trim().length > 0 &&  password.trim().length > 0  ) {
            
            props.authDataPost({
                login: name,
                password: password
            }, props)
            
            // props.history.push('/')
            // if( props.isAuth ) {
            //     return props.history.push('/')
            // }
            
            
        }

        

            
        
        // history.push('/registration')
        // onSendData()
    }


    const checkFromData = () => {
        
        
    }


    // const onSendData = () => {
    //     // const name = InputName.current.value
    //     // const password = InputNaPassword.current.value

    //     if (state.data.name === name && state.data.password === +password ) {
    //         props.loginUser()
    //         return props.history.push('/')
    //     }
    //     return setAuthData( "неверное имя или пароль" )
        

        
    // }


    // if ( props.false === false ) {
        
    // }

        const InputName = React.createRef()
        const InputNaPassword = React.createRef()
        // const history = useHistory()


        return (
            <div className = { classes.Authentication }>
                <NavBar />
                <h1>Авторизация</h1>
                
            <div className = { classes.Authentication_wrapper }>
                
                    
                    <form className = { classes.Authentication_form } onSubmit = { event => onSubmitHandler(event) }>
                <p style = {{ color: "red"}}>{ props.authError ? isAuthDataRight : null }</p>
                        
                        <input id = "authName" type = "text" className = { classes.Authentication_input } ref = { InputName } required minLength = "6" maxLength = "15" /> 
                        <label  className = { classes.inputLabel } htmlFor = "authName" >{"Логин" || <p>{isAuthDataRight}</p>}</label>   
                        <input id = "authPassword" type = "password" className = { classes.Authentication_input } ref = { InputNaPassword } required minLength = "6" maxLength = "20" />
                        <label className = { classes.inputLabel } htmlFor = "authPassword" >Пароль</label> 

                        <input  type = "submit" className = { classes.Authentication_input } value = "войти"  />
                         
                        <NavLink className = { classes.Authentication_form_register} to = "/authorization/sign_up">
                        регистрация 
                    </NavLink>
                    <NavLink className = { classes.Authentication_form_register} to = "/authorization/forgot">
                        забыл пароль 
                    </NavLink>
                    </form>

                    

                    
                </div>
                
                
            </div>
        )
}


function mapStateToProps( state ) {
    return {
        isAuth: state.AuthReducer.isAuth,
        authError: state.AuthReducer.authError
    }
}
function mapDispatchToProps( dispatch  ) {
    return {
        // loginUser: () => dispatch( loginUser() ),
        authDataPost: (data, props ) => dispatch( authDataPost( data, props ))
    }
}


export default connect(mapStateToProps, mapDispatchToProps) (withRouter(Authentication)) 