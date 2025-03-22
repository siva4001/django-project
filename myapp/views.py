from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from bson.objectid import ObjectId
from django.contrib import messages
from .db import col2  
import bcrypt

# Login view
def login(req):
    if req.method == "POST":
        useremail = req.POST.get("useremail")
        password = req.POST.get("password") 

        user = col2.find_one({"useremail": useremail})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["userpassword"].encode('utf-8')):
            req.session["useremail"] = user["useremail"]
            messages.success(req, "Login successful.")
            return redirect("home")
        else:
            messages.error(req, "Invalid email or password.")
            return redirect("login")

    return render(req, "login.html")

# Home view (after login)
def home(req):
    if req.session.get("useremail"):
        useremail = req.session.get("useremail")
        user = col2.find_one({"useremail": useremail})
        if user is not None:
            user_id = str(user["_id"])  # Get user ID
        else:
            user_id = None  # Handle the case where user is None
        return render(req, "home.html", {"user_id": user_id})
    return render(req, "home.html")

# Signup view
def signup(req):
    return render(req, "signup.html")

# Create user view (signup)
def create(req):
    if req.method == "POST":
        name = req.POST.get("name")
        age = req.POST.get("age")
        dob = req.POST.get("dob")
        phone = req.POST.get("phone")
        email = req.POST.get("email")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm-password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(req, "Passwords do not match.")
            return redirect("signup")

        if not name or not password or not phone or not email or not dob or not age:
            messages.error(req, "All fields are required.")
            return redirect("signup")

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            col2.insert_one({
                "username": name.strip(), 
                "userage": int(age),
                "userdob": dob.strip(),
                "userphone": phone.strip(),
                "useremail": email.strip(),
                "userpassword": hashed_password.decode('utf-8'),
            })
            messages.success(req, "User added successfully! Please login.")
            return redirect("login") 
        except Exception as e:
            messages.error(req, f"Error: {str(e)}")

        return redirect("signup") 

    return render(req, "home.html")

def edit(req, id):
    # Validate ID before using it
    if not id or not ObjectId.is_valid(id):
        messages.error(req, "Invalid User ID")
        return redirect("get")  # Redirect to a valid page if ID is missing or invalid

    user = col2.find_one({"_id": ObjectId(id)})
    
    if not user:
        messages.error(req, "User not found")
        return redirect("get")  # If user not found, redirect to a list page or home

    if req.method == "POST":
        updatedata = {
            "username": req.POST.get("name", user.get("username")),
            "userdob": req.POST.get("dob", user.get("userdob")),
            "useremail": req.POST.get("email", user.get("useremail")),
            "usergender": req.POST.get("gender", user.get("usergender")),
            "userphone": req.POST.get("phone", user.get("userphone")),
            "userpassword": req.POST.get("password", user.get("userpassword")),
        }
        col2.update_one({"_id": ObjectId(id)}, {"$set": updatedata})
        messages.success(req, "User updated successfully!")
        return redirect("get")  # Redirect to a page showing updated data
    
    user["id"] = str(user["_id"])  # Convert ObjectId to string for use in the template
    return render(req, "edit.html", {"edit_user": user})

# Get (List) users view
def get(req):
    try:
        getdatas = list(col2.find({}))
        for user in getdatas:
            user["id"] = str(user["_id"])  # Convert ObjectId to string for use in the template
    except Exception as e:
        messages.error(req, f"Error fetching users: {str(e)}")
        getdatas = []
    
    return render(req, "edit.html", {"getdatas": getdatas})

# Delete user view
def delete(req, id):
    try:
        col2.delete_one({"_id": ObjectId(id)})
        messages.success(req, "User deleted successfully!")
    except Exception as e:
        messages.error(req, f"Error: {str(e)}")
    
    return redirect("get")
