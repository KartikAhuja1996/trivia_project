import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
import axios from 'axios';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
      show_category_form:false,
      category:""
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  handleChange = (event) =>{
    this.setState({[event.target.name]:event.target.value});
  }


  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 3)
    console.log()
    console.log("Max Pages " + maxPage);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getCategories = ()=>{
    $.ajax({
      url:'/categories',
      type:'GET',
      success:(result)=>{
        console.log(result.categories);
        this.setState({
          categories:result.categories
        })
      }
    })
  }

  getByCategory= (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: "POST",
      success: (result) => {
        this.setState({ 
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({keyword: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  toggleCategoryForm = () => {
    this.setState({
      show_category_form:this.state.show_category_form?false:true
    });
    
  }

  onFileChange = (event) =>{
    this.setState({selectedFile:event.target.files[0]});
  }

  onSubmitCategoryForm = (event) =>{
    event.preventDefault();
    var self = this;
    var formdata = new FormData();
    if(this.state.selectedFile != null){
      formdata.append('icon',this.state.selectedFile,this.state.selectedFile.name);  
    }
    else{
      return;
    }
    formdata.append('type',this.state.category);
    axios.post('/categories',formdata).then((response)=>{
      console.log(response);
      self.getCategories();
    });
    
  }
  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {this.state.categories.map((category) => (
              <li key={category.id} onClick={() => {this.getByCategory(category.id)}}>
                {category.type}
                <img className="category" src={`/${category.type}.svg`}/>
              </li>
            ))}
          </ul>
          <p onClick={() => {this.toggleCategoryForm()} }>+ Add Category</p>
          
          <form method="POST" onSubmit={this.onSubmitCategoryForm} encType="multipart/form-data" style={{'visibility':this.state.show_category_form?'visible':'hidden'}}>
            <input type="text" name="category" placeholder="Category Name" onChange={this.handleChange}/>
            <input type="file" name="icon" onChange={this.onFileChange}/>
            <button type="submit">Add</button>
          </form>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category} 
              difficulty={q.difficulty}
              rating={q.rating}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
