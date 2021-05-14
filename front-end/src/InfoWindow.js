import React, { Component } from 'react';

export default class InfoWindow extends Component{
    constructor(props){
        super(props)
        this.state = {
            nil : ''
        }
    }
    render(){
        return(
            <template>
            <div style={{maxHeight:'1000px',weight:'250px',minWidth:'250px',textAlign:'center'}}>
            <h4>{this.props.name}</h4>

                <h4></h4>

                <h4></h4>
            </div>
            </template>
        )
    }
}