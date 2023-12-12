const express = require("express");
const { WebhookClient } = require("dialogflow-fulfillment");
const app = express();
const fetch = require("node-fetch");
const base64 = require("base-64");
const { response } = require("express");

let username = "";
let password = "";
let token = "";
let reviews = [];

USE_LOCAL_ENDPOINT = false;
// set this flag to true if you want to use a local endpoint
// set this flag to false if you want to use the online endpoint
ENDPOINT_URL = "";
if (USE_LOCAL_ENDPOINT) {
  ENDPOINT_URL = "http://127.0.0.1:5000";
} else {
  ENDPOINT_URL = "https://cs571.cs.wisc.edu";
}

async function getToken() {
  let request = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Basic " + base64.encode(username + ":" + password),
    },
  };

  const serverReturn = await fetch(ENDPOINT_URL + "/login", request);
  const serverResponse = await serverReturn.json();
  token = serverResponse.token;

  return token;
}

app.get("/", (req, res) => res.send("online"));
app.post("/", express.json(), (req, res) => {
  const agent = new WebhookClient({ request: req, response: res });

  function welcome() {
    agent.add("Webhook works!");
  }

  async function login() {
    // You need to set this as the value of the `username` parameter that you defined in Dialogflow
    username = agent.parameters.username;
    // You need to set this as the value of the `password` parameter that you defined in Dialogflow
    password = agent.parameters.password;
    await getToken();
    if(token){
      let responses = [
        "Dope, logged you in.",
        "You have been successfully logged in.",
        "Success! Logged you in!",
      ]
      let response = responses[Math.floor(Math.random()*responses.length)];
      agent.add(response)
    }
    else{
      let responses = [
        "Whoops, wrong input. Please try again.",
        "Wrong username? Wrong Password? Try again, something went wrong.",
        "Didn't work, try another username and password pair.",
      ]
      let response = responses[Math.floor(Math.random()*responses.length)];
      agent.add(response)
    }
    
  }

  async function getCategories(){
    // User has asked for all a list of all categories.
    let request = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
  
    const serverReturn = await fetch(ENDPOINT_URL + "/categories", request);
    const serverResponse = await serverReturn.json();
    let responses = [
      "Here at WiscShop we have ",
      "The categories of products available for sale are ",
      "WiscShop currently has ",
    ]
    let response = responses[Math.floor(Math.random()*responses.length)] + serverResponse.categories.join(", ");
    agent.add(response)
  }

  async function getCartInfo(){
    let request = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'x-access-token': token,
      },
    };
  
    const serverReturn = await fetch(ENDPOINT_URL + "/application/products", request);
    const serverResponse = await serverReturn.json();
    // Server response: Need response.products for list of all products
    // And within that, we can get their name and price with .price .name for each item.
    let categories = [];
    let price = 0;
    let numItems = serverResponse.products.length;
    for(let i = 0; i < serverResponse.products.length; i++){
      price += serverResponse.products[i].price*serverResponse.products[i].count;
      if(categories.includes(serverResponse.products[i].category) === false){
        categories.push(serverResponse.products[i].category)
      }      
    }
    let responses = [
      "There are " +numItems + " items in your cart. The total price is $" + price + "."
      + " Items in your cart include " + categories.join(", ") + ".",
      "Your cart currently has " + numItems + " items with a total cost of $" + price + "."
      + " There are " + categories.join(", ") +  " in your cart.",
      "Your cart is filled with " + numItems + " items to a total price of $" + price + "."
      +" Including " + categories.join(", ") + ".",
    ]   
    let response = responses[Math.floor(Math.random()*responses.length)];
    agent.add(response)
  }

  async function getProductInfo(){
    let request = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
  
    const serverReturn = await fetch(ENDPOINT_URL + "/products", request);
    const serverResponse = await serverReturn.json();
    let allItems = [];
    let allProducts = serverResponse.products;
    for(let i = 0; i < serverResponse.products.length; i++){
      allItems.push(serverResponse.products[i].name)
    }
    // See if the object parameter contained in the store
    for(let i = 0; i < agent.parameters.Object.length; i++){
      let index = allItems.indexOf(agent.parameters.Object[i])
      if(index !== -1){
        let responses = [
          "Getting info about " + agent.parameters.Object[i],
          "Sure thing! Finding info on " + agent.parameters.Object[i],
          "Of course, let me find you info on " + agent.parameters.Object[i],
        ];
        let response = responses[Math.floor(Math.random()*responses.length)];
        let description = allProducts[index].description
        response += "\nDecription:\n" + description;
        //Now, we can find the reviews as well.
        let request = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        };
        let id = allProducts[index].id
        const serverReturn = await fetch(ENDPOINT_URL + "/products/" + id + "/reviews", request);
        const serverResponse = await serverReturn.json();
        // Getting reviews/identify there are no reviews.
        if(serverResponse.reviews.length){
          reviews = serverResponse.reviews
          response += "\nWould you like to see the reviews for this item?"
        }
        else{
          reviews = [];
          response += "\nThere are no reviews for this item."
        }
        agent.add(response)
      }
      else if(i ==agent.parameters.Object.length -1){
        let responses = [
          "Whoops! We do not have that item.",
          "Couldn't find that item for you.",
          "Unsure what item you are specifying.",
        ];
        let response = responses[Math.floor(Math.random()*responses.length)]
        agent.add(response)
      }
    }
    // agent.add("nothing to see here")
  }

  async function getReviewFollowup(){
    let exampleReview = "";
    let totalStars = 0;
    // Getting a random review
    if(reviews){
      exampleReview += reviews[Math.floor(Math.random()*reviews.length)].text
    }
    // Now getting average star rating
    for(let i = 0; i < reviews.length; i++){
      totalStars += reviews[i].stars
    }
    agent.add("I found the reviews. The average rating (out of 5) was " +  (totalStars/reviews.length).toFixed(2) + " with a total of " + reviews.length + " review(s)." + "\nHere is an example review:\n" + exampleReview);
  } 

  async function getApplicationData(){
    let request = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
  
    const serverReturn = await fetch(ENDPOINT_URL + "/application", request);
    const serverResponse = await serverReturn.json();
      
  }


  async function handleNavigation(){
    if(token){
      // Now, get a list of all the categories to compare and add cart/homepage as options
      let request = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      };
    
      const serverReturn = await fetch(ENDPOINT_URL + "/categories", request);
      const serverResponse = await serverReturn.json();
      let allNavOptions = serverResponse.categories
      allNavOptions.push("cart-review")
      allNavOptions.push("cart-confirmed")
      allNavOptions.push("homepage")
      let categorySelected = "";
      categorySelected = agent.parameters.category
      // Category selected was valid. need to check through all categories that were tagged.
      for(let i = 0; i < agent.parameters.category.length; i++){
        let indexOf = allNavOptions.indexOf(categorySelected[i])
        // Correct category tagged
        let categoryEndpoint = allNavOptions[indexOf]
        // account for homepage
        if(categoryEndpoint === "homepage"){
          categoryEndpoint = "";
        }
        if(indexOf !== -1){
          let request = {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "x-access-token": token,
            },
            body: JSON.stringify({
              "back": false,
              "dialogflowUpdated": true,
              "page": "/" + username + "/" + categoryEndpoint,
            })
          };
          await fetch(ENDPOINT_URL + "/application", request);
          i = agent.parameters.category.length + 1000;
          if(categoryEndpoint === "cart-confirmed"){
            agent.add("Purchase successful. I have taken you to the confirm page to look at your purchase")
          }
          else if(categoryEndpoint === "cart-review"){
            agent.add("I have navigated you to review your cart.")
          }
          else{
            agent.add("I have navigated you to the " + categoryEndpoint + " category page.")
          }
        }
        else if(i===agent.parameters.category.length -1){
          let responses = [
            "Whoops! We do not have that item.",
            "Couldn't find that item for you.",
            "Unsure what item you are specifying.",
          ];
          let response = responses[Math.floor(Math.random()*responses.length)]
          agent.add(response)
        }
      }
    }
    else{
      let responses = [
        "You are not logged in. Cannot navigate you.",
        "Please log in before you can use wiscshop.",
        "Apologies, I cannot navigate you before you have logged in."
      ]
      let response = responses[Math.floor(Math.random()*responses.length)];
      agent.add(response);
    }

  }

  async function addCartItem(){
    let productId = await getProductID(agent.parameters.object)
    if (productId !== -1){
      let request = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'x-access-token': token,
        },
      };
    
      const serverReturn = await fetch(ENDPOINT_URL + "/application/products/" + productId, request);
      const serverResponse = await serverReturn.json();
      agent.add("The " + agent.parameters.object + " has been added to your cart.");
    }
    else{
      agent.add("Couldn't find that item for you.")
    }
  }

  async function removeCartItem(){
    let productId = await getProductID(agent.parameters.object)
    if(productId !== -1){
      let request = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          'x-access-token': token,
        },
      }; 
      const serverReturn = await fetch(ENDPOINT_URL + "/application/products/" + productId, request);
      const serverResponse = await serverReturn.json();
      if(serverResponse.message === "Product not found!"){
        agent.add("You do not have any " + agent.parameters.object + " in your cart.") 
      }
      else{
        agent.add("The " + agent.parameters.object + " has been removed from your cart.")
      }
    }
    else{
      agent.add("I couldn't understand or find any products fitting your description.")
    }
  }

  async function getProductID(productName){
    let request = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
  
    const serverReturn = await fetch(ENDPOINT_URL + "/products", request);
    const serverResponse = await serverReturn.json();
    let allItems = [];
    // getting all items in a list
    let allProducts = serverResponse.products;
    for(let i = 0; i < serverResponse.products.length; i++){
      allItems.push(serverResponse.products[i].name)
    }
    
    // See if the object parameter contained in the store
    let index = allItems.indexOf(productName)
      if(index !== -1){
        return allProducts[index].id;
      }
      else{
        return -1;
      }// agent.add("nothing to see here")
  }

  let intentMap = new Map();
  intentMap.set("Default Welcome Intent", welcome);
  // You will need to declare this `Login` intent in DialogFlow to make this work
  intentMap.set("Login", login);
  intentMap.set("Categories", getCategories);
  intentMap.set("CartInfo", getCartInfo);
  intentMap.set("ProductInfo", getProductInfo);
  intentMap.set("ProductInfo - yes", getReviewFollowup);
  intentMap.set("Navigation", handleNavigation);
  intentMap.set("AddToCart", addCartItem);
  intentMap.set("RemoveFromCart", removeCartItem);
  agent.handleRequest(intentMap);
});

app.listen(process.env.PORT || 8080);
