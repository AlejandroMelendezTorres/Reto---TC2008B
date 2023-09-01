using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;
using static System.Net.WebRequestMethods;

public class AgentController : MonoBehaviour
{
    List<List<Vector3>> positions;
    public GameObject agent1Prefab;
    public GameObject agent2Prefab;

    public JSONNode userData;

    /*    public GameObject carPrefab;
    public GameObject greenTraficLightPrefab;
    public GameObject redTraficLightPrefab;
    public GameObject yellowTraficLightPrefab;
    */

    public int clonesOfAgent1;
    public int clonesOfAgent2;

    GameObject[] agents;
    public float timeToUpdate = 5.0f;
    private float timer;
    float dt;

    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";
        //Send the request then wait here until it returns
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            // Now we check for errors
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Process the response
                userData = SimpleJSON.JSON.Parse(www.downloadHandler.text);
                //Debug.Log(userData);
                Debug.Log(userData["data"][0]["x"]);
                List<Vector3> newPositions = new List<Vector3>();
                
                //Create a list of the positions for each agent
                for (int i = 0; i < agentsList.Length; i++)
                {
                    agentsList[i] = agentsList[i].Trim();
                    if (i == 0) agentsList[i] = agentsList[i] + '}';
                    else if (i == agentsList.Length - 1) agentsList[i] = '{' + agentsList[i];
                    else agentsList[i] = '{' + agentsList[i] + '}';

                    //Debug.Log(agentsList[i]);
                    Vector3 pos = JsonUtility.FromJson<Vector3>(agentsList[i]);
                    newPositions.Add(pos);
                }

                List<Vector3> poss = new List<Vector3>();
                for(int s = 0; s < agents.Length; s++)
                {
                    //spheres[s].transform.localPosition = newPositions[s];
                    poss.Add(newPositions[s]);
                }
                positions.Add(poss);
            }
        }

    }

    // Start is called before the first frame update
    void Start()
    {
        int numOfAgents = clonesOfAgent1 + clonesOfAgent2;
        agents = new GameObject[numOfAgents];
        for(int i = 0; i < numOfAgents; i++)
        {
            if(i < clonesOfAgent1)
            {
                agents[i] = Instantiate(agent1Prefab, Vector3.zero, Quaternion.identity);
            }
            else
            {
                agents[i] = Instantiate(agent2Prefab, Vector3.zero, Quaternion.identity);
            }
        }


        positions = new List<List<Vector3>>();
        Debug.Log(agents.Length);
#if UNITY_EDITOR
        //string call = "WAAAAASSSSSAAAAAAAAAAP?";
        Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        //StartCoroutine(SendData(call));
        StartCoroutine(SendData(json));
        timer = timeToUpdate;
#endif
    }

    // Update is called once per frame
    void Update()
    {
        /*
         *    5 -------- 100
         *    timer ----  ?
         */
    timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if(timer < 0)
        {
#if UNITY_EDITOR
            timer = timeToUpdate; // reset the timer
            Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine(SendData(json));
#endif
        }


        if (positions.Count > 1)
        {
            for (int s = 0; s < agents.Length; s++)
            {
                // Get the last position for s
                List<Vector3> last = positions[positions.Count - 1];
                // Get the previous to last position for s
                List<Vector3> prevLast = positions[positions.Count - 2];
                // Interpolate using dt
                Vector3 interpolated = Vector3.Lerp(prevLast[s], last[s], dt);
                agents[s].transform.localPosition = interpolated;

                Vector3 dir = last[s] - prevLast[s];
                agents[s].transform.rotation = Quaternion.LookRotation(dir);
            }
        }
    }
}
