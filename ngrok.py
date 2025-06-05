# Windows Debug and Fix for ngrok ERR_NGROK_3200
# Save as: debug_server.py

import subprocess
import sys
import time
import threading
import requests
from pyngrok import ngrok

def check_port_available(port):
    """Check if port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def test_local_server(port):
    """Test if server is responding locally"""
    try:
        response = requests.get(f'http://127.0.0.1:{port}', timeout=5)
        return True, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

def run_server_with_logging():
    """Run server with proper error logging"""
    try:
        print("🚀 Starting server...")
        
        # Check if file exists
        import os
        if not os.path.exists('ws_1.py'):
            print("❌ ws_1.py file not found!")
            print(f"📁 Current directory: {os.getcwd()}")
            print(f"📁 Files in directory: {os.listdir('.')}")
            return
        
        # Execute the server file
        with open('ws_1.py', 'r') as f:
            server_code = f.read()
            print(f"✅ Server file loaded ({len(server_code)} characters)")
        
        exec(open('ws_1.py').read())
        
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main debug function"""
    print("🐛 Debugging ngrok ERR_NGROK_3200 on Windows")
    print("=" * 50)
    
    # Step 1: Check if port 8000 is available
    print("🔍 Step 1: Checking port availability...")
    port = 8000
    if check_port_available(port):
        print(f"✅ Port {port} is available")
    else:
        print(f"❌ Port {port} is already in use!")
        print("💡 Try killing processes using port 8000:")
        print("   netstat -ano | findstr :8000")
        print("   taskkill /PID <PID_NUMBER> /F")
        return
    
    # Step 2: Setup ngrok
    print("\n🔧 Step 2: Setting up ngrok...")
    try:
        ngrok.set_auth_token("2y4nBAGeqa4wdXQOC7v1IPnRk5y_6WbMyh6P5aSbneYgKz6TR")
        ngrok.kill()  # Kill existing tunnels
        print("✅ ngrok configured")
    except Exception as e:
        print(f"❌ ngrok setup failed: {e}")
        return
    
    # Step 3: Start server with proper logging
    print("\n🚀 Step 3: Starting server...")
    server_thread = threading.Thread(target=run_server_with_logging, daemon=True)
    server_thread.start()
    
    # Step 4: Wait and test local server
    print("\n⏳ Step 4: Testing local server...")
    for i in range(10):  # Wait up to 10 seconds
        time.sleep(1)
        is_running, result = test_local_server(port)
        if is_running:
            print(f"✅ Local server is responding! Status: {result}")
            break
        else:
            print(f"⏳ Attempt {i+1}: {result}")
    else:
        print("❌ Local server never started responding!")
        print("💡 Check your ws_1.py file - the server might have errors")
        return
    
    # Step 5: Create ngrok tunnel
    print("\n🌐 Step 5: Creating ngrok tunnel...")
    try:
        public_url = ngrok.connect(port)
        print(f"✅ Tunnel created: {public_url}")
        
        # Step 6: Test public URL
        print("\n🧪 Step 6: Testing public URL...")
        time.sleep(2)  # Give ngrok a moment
        
        try:
            response = requests.get(f"{public_url}", timeout=10, headers={
                "ngrok-skip-browser-warning": "true"
            })
            print(f"✅ Public URL works! Status: {response.status_code}")
            print(f"🎉 SUCCESS! Your server is publicly accessible")
            print(f"🔗 Public URL: {public_url}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Public URL test failed: {e}")
            print("💡 This might be a temporary ngrok issue - try again")
            
    except Exception as e:
        print(f"❌ Tunnel creation failed: {e}")
        return
    
    # Keep running
    print(f"\n⏰ Server running... Press Ctrl+C to stop")
    try:
        while True:
            time.sleep(30)
            # Test both local and public URLs periodically
            local_ok, _ = test_local_server(port)
            print(f"⏰ Status - Local: {'✅' if local_ok else '❌'} | Public: {public_url}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        ngrok.kill()
        print("✅ Stopped")

if __name__ == "__main__":
    main()
