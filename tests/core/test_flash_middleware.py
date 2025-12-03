import pytest
from unittest.mock import patch, MagicMock
from django.contrib.messages import constants as message_constants
from django.contrib.messages.storage.base import Message
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser

from apps.core.middleware import InertiaFlashMessagesMiddleware
from tests.factories import UserFactory

@pytest.mark.unit
def test_flash_middleware_unauthenticated(rf):
    """Test that middleware does nothing for unauthenticated users."""
    request = rf.get("/")
    request.user = AnonymousUser()
    
    get_response = MagicMock(return_value=HttpResponse())
    middleware = InertiaFlashMessagesMiddleware(get_response)
    
    with patch('apps.core.middleware.share') as mock_share:
        middleware(request)
        mock_share.assert_not_called()

@pytest.mark.unit
@pytest.mark.django_db
def test_flash_middleware_authenticated_no_messages(rf):
    """Test that middleware shares empty flash list when no messages exist."""
    request = rf.get("/")
    request.user = UserFactory()
    
    # Setup session
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    
    # Mock messages
    with patch('django.contrib.messages.get_messages', return_value=[]):
        get_response = MagicMock(return_value=HttpResponse())
        middleware = InertiaFlashMessagesMiddleware(get_response)
        
        with patch('apps.core.middleware.share') as mock_share:
            middleware(request)
            
            mock_share.assert_called_once()
            call_kwargs = mock_share.call_args[1]
            assert call_kwargs['flash'] == []
            assert call_kwargs['errors'] == {}

@pytest.mark.unit
@pytest.mark.django_db
def test_flash_middleware_authenticated_with_messages(rf):
    """Test that middleware correctly formats and shares messages."""
    request = rf.get("/")
    request.user = UserFactory()
    
    # Setup session
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    
    # Create mock messages
    mock_messages = [
        Message(message_constants.SUCCESS, "Operation successful"),
        Message(message_constants.ERROR, "Something went wrong"),
    ]
    
    with patch('django.contrib.messages.get_messages', return_value=mock_messages):
        get_response = MagicMock(return_value=HttpResponse())
        middleware = InertiaFlashMessagesMiddleware(get_response)
        
        with patch('apps.core.middleware.share') as mock_share:
            middleware(request)
            
            mock_share.assert_called_once()
            call_kwargs = mock_share.call_args[1]
            flash_data = call_kwargs['flash']
            
            assert len(flash_data) == 2
            assert flash_data[0] == {'type': 'success', 'message': 'Operation successful'}
            assert flash_data[1] == {'type': 'error', 'message': 'Something went wrong'}

@pytest.mark.unit
@pytest.mark.django_db
def test_flash_middleware_includes_session_errors(rf):
    """Test that middleware includes errors from session."""
    request = rf.get("/")
    request.user = UserFactory()
    
    # Setup session with errors
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session['errors'] = {'field': 'Invalid value'}
    request.session.save()
    
    with patch('django.contrib.messages.get_messages', return_value=[]):
        get_response = MagicMock(return_value=HttpResponse())
        middleware = InertiaFlashMessagesMiddleware(get_response)
        
        with patch('apps.core.middleware.share') as mock_share:
            middleware(request)
            
            call_kwargs = mock_share.call_args[1]
            assert call_kwargs['errors'] == {'field': 'Invalid value'}
