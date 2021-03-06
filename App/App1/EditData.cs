﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;

using MySql.Data.MySqlClient;

namespace LastResortForReal
{
	[Activity(Label = "EditData")]
	public class EditData : Activity
	{
		protected override void OnCreate(Bundle savedInstanceState)
		{
			base.OnCreate(savedInstanceState);

			// Create your application here
			SetContentView(Resource.Layout.EditEntry);
			var roomData = Intent.Extras.GetString("roomData");
			MySqlConnection connection = new MySqlConnection("Server=sql9.freemysqlhosting.net;" +
															 "Port=3306;" +
															 "Database=sql9146891;" +
															 "User Id=sql9146891;" +
															 "Password=3FbDmkqFFE;" +
															 "charset=utf8");
			connection.Open();

			TextView RoomTitle = FindViewById<TextView>(Resource.Id.RoomTitle);
			RoomTitle.Text = "Room name that will be changed";
			TextView TitleRoomNameID = FindViewById<TextView>(Resource.Id.curentRoomname);
			TitleRoomNameID.Text = roomData;
			EditText updateInfo = FindViewById<EditText>(Resource.Id.UpdateInfo);

			Button updatebtn = FindViewById<Button>(Resource.Id.Updatebtn);
			updatebtn.Click += delegate
			{
				MySqlCommand update = new MySqlCommand("UPDATE homeinfo SET roomname='" + updateInfo.Text.Replace("'", "''") +
													   "' WHERE roomName = '" + TitleRoomNameID.Text.Replace("'", "''") +
													   "'", connection);
				update.ExecuteNonQuery();
				StartActivity(typeof(MainActivity));
			};
		}
	}
}