package com.example.leonvillapun.SyncTaskClass;

import android.app.ProgressDialog;
import android.content.Context;
import android.media.session.MediaSession;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import com.google.api.client.extensions.android.http.AndroidHttp;
import com.google.api.client.json.gson.GsonFactory;
import com.tactic_api.TacticApi;
import com.tactic_api.model.MessagesTacticInput;
import com.tactic_api.model.MessagesCodeMessage;

/**
 * Created by adsoft on 14/11/17.
 */

public class tweetSyncTask extends AsyncTask<String,Void,MessagesCodeMessage> {

    Context context;
    private ProgressDialog pd;
    MessagesCodeMessage respuesta;

    public tweetSyncTask(Context context) {this.context = context; }

    @Override
    protected void onPreExecute()
    {
        super.onPreExecute();
        pd = new ProgressDialog(context);
        pd.setMessage("Login");
        pd.show();
    }




    @Override
    protected MessagesCodeMessage doInBackground(String... params) {

        respuesta = new MessagesCodeMessage();
        try
        {
            TacticApi.Builder builder =
                    new TacticApi.Builder(AndroidHttp.newCompatibleTransport(), new GsonFactory(), null);
            TacticApi service = builder.build();
            MessagesTacticInput log = new MessagesTacticInput();
            //params es una lista de strings que funciona como argv
            //[0] = email, [1] = password
            log.setTitle(params[0]);
            log.setDescription(params[1]);
            log.setCategory(params[2]);
            log.setSolution(params[3]);
            log.setToken(params[4]);
            log.setUrlImage(params[5]);
            respuesta = service.tactic().insert(log).execute();
        }
        catch (Exception e)
        {
            Log.d("Error al insertar tweet", e.getMessage(), e);
        }
        finally
        {
            return respuesta;
        }
    }


    @Override
    protected void onPostExecute(MessagesCodeMessage messagesTokenMessage)
    {
        pd.dismiss();
        if(respuesta.getCode() == 1)
            Toast.makeText(this.context, "Insert succesfully " + respuesta.getMessage(), Toast.LENGTH_SHORT).show();
        else
            Toast.makeText(this.context,"Error at insert tweet !!!",Toast.LENGTH_SHORT).show();
    }
}

