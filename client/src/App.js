import React from 'react';

import { Route, Redirect } from "react-router-dom"

import Authentication from "./pages/Authentication/Authentication"
import Registration from "./pages/Registration/Registration"
import RecoverPassword from "./pages/RecoverPassword/RecoverPassword"
import ConfirmChangePassword from "./pages/ConfirmChangePassword/ConfirmChangePassword"
import MainPage from "./pages/MainPage/MainPage"

import Quiz from "./pages/Quiz/Quiz"
import QuizBlock from "./pages/QuizBlock/QuizBlock"
import { connect } from 'react-redux';



// <Route  path = "/:course/:id" > <QuizBlock />  </Route>

function App( props ) {

  const AuthRouterHandler = () => {
    if( props.isAuth ) {
      return (
        <React.Fragment>
          <Route exact path = "/:course" > <Quiz />  </Route>



          <Route exact path = "/"  > <MainPage /> </Route>
        </React.Fragment>
        
      )} else {
        return(
          <React.Fragment>
          
            <Route  path = "/authorization/sign_up" > <Registration /> </Route>
            <Route  path = "/authorization/log_in" >  <Authentication />  </Route>
            
            <Route path = "/authorization/forgot" > <RecoverPassword />  </Route>
            <Route path = "/authorization/confirm_new_password" > <ConfirmChangePassword />  </Route>
            <Route exact path = "/:course" > <Quiz /> </Route>
             <Route   path = "/:course/:id" > <QuizBlock /> </Route>
            <Route exact path = "/"  > <MainPage /> </Route>
          </React.Fragment>
          
        )
      }
    
  }
  
  
  
  return (
    <div className="App">
 
      { AuthRouterHandler() }
      
 
    
    


    </div>
  );
}


function mapStateToProps( state ) {
  
  return {
    isAuth: state.AuthReducer.isAuth
  }
}


function mapDispatchToProps( dispatch ) {
  return {
    
  }
}

export default connect(mapStateToProps, mapDispatchToProps ) (App);
