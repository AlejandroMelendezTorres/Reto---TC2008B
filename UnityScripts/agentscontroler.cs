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
    List<List<Vector3>> positions = new List<List<Vector3>>();
    List<Vector3> traficLightPositions = new List<Vector3>();

    public JSONNode userData;

    public GameObject carPrefab;
    public GameObject greenLightPrefab;
    public GameObject redLightPrefab;
    public GameObject yellowLightPrefab;

    List<int> lightsColor = new List<int>();
    List<int> newLights = new List<int>();
    

    List<GameObject> agents = new List<GameObject>();
    List<GameObject> Lights = new List<GameObject>();

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
                Debug.Log(userData);
                //Debug.Log(userData["data"][0]["x"]);
                List<Vector3> newPositions = new List<Vector3>();

                //get the number of objects in the data array
                int numOfObjects = userData["data"].Count;
                
                
                //Create a list of the positions for each agent
                for (int i = 0; i < numOfObjects; i++)
                {
                    //Debug.Log(userData["data"][i]);
                    float x = userData["data"][i]["x"];
                    float y = userData["data"][i]["y"];
                    float z = userData["data"][i]["z"];

                    Vector3 pos = new Vector3(x, y, z);

                    if (userData["data"][i]["type"] == "car")
                    {
                        newPositions.Add(pos);
                    }
                    else if (userData["data"][i]["type"] == "trafficLight")
                    {
                        traficLightPositions.Add(pos);
                        newLights.Add(userData["data"][i]["color"]);
                    }      
                }
                positions.Add(newPositions);
            }
        }
        yield return null;
    }

    // Start is called before the first frame update
    IEnumerator Start()
    {
        //Get the first data from Python
        string json = EditorJsonUtility.ToJson("");
        yield return StartCoroutine(SendData(json));
        timer = timeToUpdate;
        innitAgents();
    }
    
    // Update is called once per frame
    void Update()
    {
        /*
    timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if(timer < 0)
        {
            traficLightPositions.Clear();
            newLights.Clear();
            string json = EditorJsonUtility.ToJson("");
            StartCoroutine(SendData(json));
            timer = timeToUpdate;
        }
        switchLight();

        if (positions.Count > 1)
        {
            for (int s = 0; s < positions.Count; s++)
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
        */
    }

    void switchLight()
    {
        for (int i =0; i<4; i++)
        {
            if (newLights[i] != lightsColor[i])
            {
                if (newLights[i] == 2)
                {
                    GameObject tLight = Instantiate(greenLightPrefab, traficLightPositions[i], Quaternion.identity);
                    Lights[i] = tLight;
                }
                else if (newLights[i] == 1)
                {
                    GameObject tLight = Instantiate(yellowLightPrefab, traficLightPositions[i], Quaternion.identity);
                    Lights[i] = tLight;
                }
                else if (newLights[i] == 0)
                {
                    GameObject tLight = Instantiate(redLightPrefab, traficLightPositions[i], Quaternion.identity);
                    Lights[i] = tLight;
                }
                lightsColor[i] = newLights[i];
            }
        }
    }
    void innitAgents()
    {
        //Create the agents and lights
        lightsColor = newLights;
        newLights.Clear();
        Debug.Log(lightsColor);
        for (int i = 0; i < 4; i++)
        {
            if (lightsColor[i] == 2)
            {
                GameObject tLight = Instantiate(greenLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
            else if (lightsColor[i] == 1)
            {
                GameObject tLight = Instantiate(yellowLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
            else if (lightsColor[i] == 0)
            {
                GameObject tLight = Instantiate(redLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
        }
        foreach (Vector3 carPosition in positions[0])
        {
            GameObject newCar = Instantiate(carPrefab, carPosition, Quaternion.identity);
            agents.Add(newCar);
        }

    }
}
