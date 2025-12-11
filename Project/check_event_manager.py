#!/usr/bin/env python3
"""
Script to check and fix event manager login issues
"""

from app import app
from models import db, EventManager
from werkzeug.security import check_password_hash

def check_event_managers():
    """Check event manager accounts and fix passwords"""
    print("=== Checking Event Manager Accounts ===\n")
    
    with app.app_context():
        try:
            # Get all event managers
            managers = EventManager.query.all()
            print(f"Found {len(managers)} event managers\n")
            
            if len(managers) == 0:
                print("❌ No event managers found in database!")
                return False
            
            # Check first few managers
            print("Checking first 5 event managers:")
            print("-" * 60)
            
            for i, manager in enumerate(managers[:5], 1):
                print(f"\n{i}. Email: {manager.email}")
                print(f"   Name: {manager.first_name} {manager.last_name}")
                print(f"   Active: {manager.is_active}")
                print(f"   Password hash: {manager.password_hash[:30]}...")
                
                # Check if password works
                if manager.check_password('admin123'):
                    print(f"   ✅ Password 'admin123' works")
                else:
                    print(f"   ❌ Password 'admin123' does NOT work")
                    print(f"   🔧 Fixing password...")
                    manager.set_password('admin123')
                    db.session.add(manager)
                    print(f"   ✅ Password fixed!")
            
            # Check aaron.manager specifically
            aaron = EventManager.query.filter_by(email='aaron.manager@comedyorg.com').first()
            if aaron:
                print(f"\n{'='*60}")
                print(f"Checking aaron.manager@comedyorg.com specifically:")
                print(f"   Active: {aaron.is_active}")
                print(f"   Password hash: {aaron.password_hash[:30]}...")
                if aaron.check_password('admin123'):
                    print(f"   ✅ Password 'admin123' works")
                else:
                    print(f"   ❌ Password 'admin123' does NOT work")
                    print(f"   🔧 Fixing password...")
                    aaron.set_password('admin123')
                    db.session.add(aaron)
                    print(f"   ✅ Password fixed!")
            else:
                print(f"\n❌ aaron.manager@comedyorg.com not found!")
            
            # Fix all event manager passwords
            print(f"\n{'='*60}")
            print("Fixing all event manager passwords...")
            fixed_count = 0
            for manager in managers:
                if not manager.password_hash or manager.password_hash.startswith('$2y$10$hash'):
                    manager.set_password('admin123')
                    db.session.add(manager)
                    fixed_count += 1
                    print(f"✅ Fixed: {manager.email}")
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n{'='*60}")
            print(f"✅ Fixed {fixed_count} event manager passwords")
            print(f"✅ Total event managers: {len(managers)}")
            print(f"\nAll event managers now have password: 'admin123'")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    if check_event_managers():
        print("\n✅ Event manager check completed successfully!")
        print("\nYou can now login with:")
        print("   Email: aaron.manager@comedyorg.com")
        print("   Password: admin123")
    else:
        print("\n❌ Event manager check failed!")

