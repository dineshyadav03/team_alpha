import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:3000"  # Update this if your frontend runs on a different port

def test_frontend_connection():
    """Test if frontend is accessible"""
    try:
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        print("✅ Frontend is accessible")
        return True
    except Exception as e:
        print(f"❌ Frontend connection failed: {str(e)}")
        return False

def test_chat_api():
    """Test chat API endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "What are the HSA regulations?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        print("✅ Chat API is working")
        return True
    except Exception as e:
        print(f"❌ Chat API test failed: {str(e)}")
        return False

def test_document_upload():
    """Test document upload functionality"""
    try:
        # Create a test file
        test_file = "test_document.txt"
        with open(test_file, "w") as f:
            f.write("This is a test document for HSA regulations.")
        
        # Test file upload
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/api/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✅ Document upload is working")
        
        # Clean up test file
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"❌ Document upload test failed: {str(e)}")
        return False

def test_search_functionality():
    """Test search functionality"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/search",
            json={"query": "HSA regulations"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        print("✅ Search functionality is working")
        return True
    except Exception as e:
        print(f"❌ Search test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all frontend tests"""
    print("Starting frontend tests...")
    
    tests = [
        ("Frontend Connection", test_frontend_connection),
        ("Chat API", test_chat_api),
        ("Document Upload", test_document_upload),
        ("Search Functionality", test_search_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n=== Test Summary ===")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

if __name__ == "__main__":
    run_all_tests() 