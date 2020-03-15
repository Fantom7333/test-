import React from 'react'
import { NavLink } from "react-router-dom"

import classes from "./NavBar.module.css"

import Button from '@material-ui/core/Button'
import { makeStyles } from '@material-ui/core/styles';



import logo from "../../../images/logotip.png"
import settings from "../../../images/nastroyki.png"
import { connect } from 'react-redux';

import { logoutUser } from "../../../store/actions/AuthAction"


const useStyles = makeStyles({
    root: {
        margin: "0 10px"
    }
})



function NavBar(props) {

    const materClasses = useStyles()


    console.log( props.isAuth )
    const navButtonsHandler = (  ) => {
        if( props.isAuth ) {
            return (
                <>
                    <NavLink to = "/">
                        <Button onClick = { () => props.logoutUser() } className = { materClasses.root } variant="contained" color="primary" >выход</Button>
                    </NavLink>
                </>
            )        
        } else {
            return (
                <>
                    <NavLink to = "/authorization/log_in">
                        <Button className = { materClasses.root } variant="contained" color="primary" >вход</Button>
                    </NavLink>
                

                    <NavLink to = "/authorization/sign_up">
                        <Button className = { materClasses.root } variant="contained" color="primary" >регистрация</Button>
                    </NavLink>
                </>    
            )
        }
    }


    return (
        <div className = { classes.NavBar }>

            <NavLink to = "/" > <img src = {logo} alt = "логотип компании"/> </NavLink>

            <div className = { classes.NavBar_LogIn_And_Register}>
                <img src = {settings} alt = "" />
                
                { navButtonsHandler() }
            </div>
            
        </div>
    )
}


function mapStateToProps( state ) {
    
    return {
      isAuth: state.AuthReducer.isAuth
    }
  }
  
  
  function mapDispatchToProps( dispatch ) {
    return {
        logoutUser: () => dispatch( logoutUser() )
    }
  }
  
  export default connect(mapStateToProps, mapDispatchToProps ) (NavBar);
  
