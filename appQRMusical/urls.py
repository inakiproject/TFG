from django.conf.urls import include, url
from appQRMusical.views import Home, Identify, Disconnect, Settings, Game_settings, Play, Songs, List, Gallery, Multimedia_detail, Multimedia_delete, Players_list, Users_list, Update_player, Update_user, User_ID, Multi_ID, Multi_ID_delete, Create_player, Create_user, Multimedia_update, Player_delete, ID_delete, User_delete, User, Match, Match_list, Identify_ID, Therapists_list, Treatments_list, Therapies_list, Create_therapist, Create_treatment, Treatment_delete, Update_treatment, Diagnostic_list, Create_diagnostic, Update_diagnostic, Delete_diagnostic, Create_therapy, Update_therapy, Therapy_delete, Activity_settings, Indicators_list, Create_indicator, Update_indicator, Indicator_delete, Categories_list, Update_category, Category_delete, Create_category, Add_category_player, Results, Results_details, Add_therapy_player, Therapy_player_list,  Delete_therapy_player
from . import views

# For load images in dev mode
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	# Home
	url(r'^$', Home.as_view(), name='home'),	

	# Identify
	url(r'^identify/$', Identify, name='identify'),
	url(r'^disconnect/$', Disconnect, name='disconnect'),	

	# Play-Songs
	url(r'^play/$', Play.as_view(), name='play'),	
	url(r'^play/songs_list/$', Songs.as_view(), name='songs_list'),	
	url(r'^play/songs_list/(?P<id_player>\d+)/player_game/$', views.player_game, name='player_game'),	
	url(r'^play/songs_list/(?P<id_player>\d+)/player_game_matching/$', views.player_game_matching, name='player_game_matching'),	
	url(r'^play/songs_list/(?P<id_player>\d+)/player_game/player_game_song$', views.player_game_song, name='player_game_song'),	

    #Play-Match
	url(r'^play/match_game_list/$', List.as_view(), name='list'),
	url(r'^play/match_game_list/(?P<id_player>\d+)/match_game/$', views.match_game, name='match_game'),	
	url(r'^play/match_game_list/(?P<id_player>\d+)/match_game_matching/$', views.match_game_matching, name='match_game_matching'),	
	#url(r'^play/match_game_list/(?P<id_player>\d+)/match_game_image/$', views.match_game_image, name='match_game_image'),	

    # Login
	url(r'^login/$', views.Login, name='login'),
	url(r'^logout/$', views.Logout, name='logout'), 	

	# Settings
	url(r'^settings/$', Settings.as_view(), name='settings'),
	url(r'^settings/Activities/$', Activity_settings.as_view(), name='activity_settings'),
	url(r'^settings/Games/$', Game_settings.as_view(), name='game_settings'), 
	url(r'^settings/Categories/$', Categories_list.as_view(), name='categories_list'),
	url(r'^settings/Categories/(?P<pk>\d+)/update/$', Update_category.as_view(), name='update_category'),
	url(r'^settings/Categories/(?P<pk>\d+)/delete/$', Category_delete.as_view(), name='category_delete'), 
	url(r'^settings/Categories/create/$', Create_category.as_view(), name='create_category'),

	# Settings - Therapy-Activity
	url(r'^settings/Activities/therapy-player/$', Therapy_player_list.as_view(), name='therapy_player'), 
	url(r'^settings/Activities/therapy-player/details/$', Add_therapy_player.as_view(), name='add_therapy_player'), 
	url(r'^settings/Activities/therapy-player/(?P<pk>\d+)/delete/$', Delete_therapy_player.as_view(), name='delete_therapy_player'), 

	# Settings - Results
	url(r'^settings/Results/$', Results.as_view(), name='results'),
	url(r'^settings/Results/(?P<pk>\d+)/Details/$', Results_details, name='results_details'),

	# Settings - Gallery
	url(r'^settings/gallery/$', Gallery.as_view(), name='gallery'), 
	url(r'^settings/gallery/multimedia_detail/(?P<pk>\d+)/$', Multimedia_detail.as_view(), name='multimedia_detail'), 
	url(r'^settings/gallery/multimedia_update/(?P<pk>\d+)/$', Multimedia_update.as_view(), name='multimedia_update'), 	
	url(r'^settings/gallery/(?P<pk>\d+)/delete/$', Multimedia_delete.as_view(), name='multimedia_delete'), 	
	url(r'^settings/gallery/upload/$', views.upload_multimedia, name='upload_multimedia'), 
	url(r'^settings/gallery/multimedia_id/(?P<pk>\d+)/$', Multi_ID, name='multi_id'),
	url(r'^settings/gallery/multimedia_id_clean/(?P<pk>\d+)/$', Multi_ID_delete, name='multi_id_delete'), 

	# Settings - Music Game
	url(r'^settings/players_list/$', Players_list.as_view(), name='players_list'), 
	url(r'^settings/players_list/(?P<pk>\d+)/update/$', Update_player.as_view(), name='update_player'),
	url(r'^settings/players_list/category_player/$', Add_category_player.as_view(), name='add_category_player'), 
	url(r'^settings/players_list/(?P<pk>\d+)/delete/$', Player_delete.as_view(), name='player_delete'), 
	url(r'^settings/players_list/create/$', Create_player.as_view(), name='create_player'), 
	url(r'^settings/players_list/(?P<id>\d+)/add_multimedia_to_player/$', views.add_multimedia_to_player, name='add_multimedia_to_player'), 
	url(r'^settings/players_list/(?P<id_player>\d+)/add_multimedia_to_player/(?P<id_multimedia>\d+)/$', views.add_multimedia_to_player_function, name='add_multimedia_to_player_function'), 
	url(r'^settings/players_list/(?P<id_player>\d+)/update/(?P<id_multimedia>\d+)/$', views.del_multimedia_of_player_function, name='del_multimedia_of_player_function'), 

	# Settings - Match Game
	url(r'^settings/match_list/$', Match_list.as_view(), name='match_list'), 
	#url(r'^settings/match_list/(?P<pk>\d+)/update/$', Update_match_list.as_view(), name='update_match_list'), 
	#url(r'^settings/match_list/(?P<pk>\d+)/delete/$', Delete_match_list.as_view(), name='delete_match_list'),
	#url(r'^settings/match_list/create/$', Create_match_list.as_view(), name='create_match_list'), 

	# Settigns - Camera
	url(r'^settings/camera/$', views.camera, name='camera'), 

	# Settigns - User	
	url(r'^settings/user/$', User.as_view(), name='user'),
	url(r'^settings/user/edit_name/$', views.edit_name, name='edit_name'), 
	url(r'^settings/user/edit_email/$', views.edit_email, name='edit_email'), 
	url(r'^settings/user/edit_password/$', views.edit_password, name='edit_password'), 

    # Settigns - Users
	url(r'^settings/users_list/$', Users_list.as_view(), name='users_list'), 
	url(r'^settings/users_list/(?P<pk>\d+)/update/$', Update_user.as_view(), name='update_user'), 
	url(r'^settings/users_list/(?P<pk>\d+)/modID/$', User_ID, name='user_id'), 
	url(r'^settings/users_list/(?P<pk>\d+)/delete/$', User_delete.as_view(), name='user_delete'),
	url(r'^settings/users_list/(?P<pk>\d+)/IDdelete/$', ID_delete, name='id_delete'), 
	url(r'^settings/users_list/create/$', Create_user.as_view(), name='create_user'), 

    # Settigns - Treatments
	url(r'^settings/treatments_list/$', Treatments_list, name='treatments_list'),
	url(r'^settings/treatments_list/create/$', Create_treatment, name='create_treatment'),
	url(r'^settings/treatmentss_list/(?P<pk>\d+)/update/$', Update_treatment.as_view(), name='update_treatment'),
	url(r'^settings/treatmentss_list/(?P<pk>\d+)/delete/$', Treatment_delete.as_view(), name='treatment_delete'),

    # Settigns - Therapies
	url(r'^settings/therapies_list/$', Therapies_list, name='therapies_list'),
	url(r'^settings/therapies_list/create$', Create_therapy, name='create_therapy'), 
	url(r'^settings/therapies_list/(?P<pk>\d+)/update$', Update_therapy.as_view(), name='update_therapy'), 
	url(r'^settings/therapies_list/(?P<pk>\d+)/delete$', Therapy_delete.as_view(), name='therapy_delete'), 

    # Settigns - Diagnostic
	url(r'^settings/user/(?P<pk>\d+)/diagnostic_list/$', Diagnostic_list, name='diagnostic_list'), 
	url(r'^settings/user/(?P<pk>\d+)/diagnostic_create/$', Create_diagnostic, name='create_diagnostic'),
	url(r'^settings/user/(?P<pk>\d+)/update_diagnostic/$', Update_diagnostic.as_view(), name='update_diagnostic'), 
	url(r'^settings/user/(?P<pk>\d+)/delete_diagnostic/$', Delete_diagnostic.as_view(), name='delete_diagnostic'), 
    
	#Settigns - Therapists
	url(r'^settings/therapists_list/$', Therapists_list, name='therapists_list'), 
	url(r'^settings/create_therapists/$', Create_therapist.as_view(), name='create_therapist'), 

	#Settings - Indicators
	url(r'^settings/activities/indicators/$', Indicators_list.as_view(), name='indicators_list'),
	url(r'^settings/activities/indicators/create/$', Create_indicator.as_view(), name='create_indicator'),
	url(r'^settings/activities/indicators/(?P<pk>\d+)/update/$', Update_indicator.as_view(), name='update_indicator'),
	url(r'^settings/activities/indicators/(?P<pk>\d+)/delete/$', Indicator_delete.as_view(), name='indicator_delete'),  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
