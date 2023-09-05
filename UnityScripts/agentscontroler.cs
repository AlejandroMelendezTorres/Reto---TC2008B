using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class AgentController : MonoBehaviour
{
    List<Vector3> traficLightPositions = new List<Vector3>();

    public JSONNode userData;

    public GameObject carPrefab;
    /*
    public GameObject carPrefab1;
    public GameObject carPrefab2;
    public GameObject carPrefab3;
    public GameObject carPrefab4;
    public GameObject carPrefab5;
    public GameObject carPrefab6;
    List<GameObject> carPrefabs = new List<GameObject>();
    */

    public GameObject greenLightPrefab;
    public GameObject redLightPrefab;
    public GameObject yellowLightPrefab;



    List<int> lightsColor = new List<int>();
    List<int> newLights = new List<int>();

    Dictionary<int, GameObject> carAgents = new Dictionary<int, GameObject>();

    Dictionary<int, Vector3> carPositions;
    Dictionary<int, Vector3> newCarPositions = new Dictionary<int, Vector3>();

    Dictionary<int, GameObject> lightAgents = new Dictionary<int, GameObject>();
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
                //Debug.Log(userData["data"][0]["x"]);
                //List<Vector3> newPositions = new List<Vector3>();

                //get the number of objects in the data array
                int numOfObjects = userData["data"].Count;
                newCarPositions.Clear();

                //Create a list of the positions for each agent

                for (int i = 0; i < numOfObjects; i++)
                {
                    int id = userData["data"][i]["ID"];
                    //Debug.Log(userData["data"][i]);
                    float x = userData["data"][i]["x"];
                    float y = userData["data"][i]["y"];
                    float z = userData["data"][i]["z"];

                    Vector3 pos = new Vector3(x, y, z);

                    if (userData["data"][i]["type"] == 0)//if the object is a car
                    {
                        //newPositions.Add(pos);
                        newCarPositions[id] = pos;
                    }
                    else if (userData["data"][i]["type"] == 1)//if the object is a trafic light
                    {
                        traficLightPositions.Add(pos);
                        newLights.Add(userData["data"][i]["color"]);
                    }
                }
                //positions.Add(newPositions);
            }
        }
        //Debug.Log("Done");
        yield return null;
    }

    // Start is called before the first frame update
    IEnumerator Start()
    {
        /*
        //Innit the car prefabs
        carPrefabs.Add(carPrefab1);
        carPrefabs.Add(carPrefab2);
        carPrefabs.Add(carPrefab3);
        carPrefabs.Add(carPrefab4);
        carPrefabs.Add(carPrefab5);
        carPrefabs.Add(carPrefab6);
        */

        //Get the first data from Python
        string json = EditorJsonUtility.ToJson("");
        yield return StartCoroutine(SendData(json));
        timer = timeToUpdate;
        InnitAgents();
    }

    // Update is called once per frame
    void Update()
    {

        timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if (timer < 0)
        {
            _ = StartCoroutine(UpdateData());
            timer = timeToUpdate;
        }


    }
    IEnumerator UpdateData()
    {
        Debug.Log("Update");
        traficLightPositions.Clear();
        lightsColor.Clear();
        newLights.Clear();
        string json = EditorJsonUtility.ToJson("");
        yield return StartCoroutine(SendData(json));
        SwitchLight();
        UpdateCars();
    }


    void SwitchLight()
    {
        lightsColor = new List<int>(newLights);
        foreach (GameObject light in Lights)
        {
            Destroy(light);
        }
        Lights.Clear();
        for (int i = 0; i < 4; i++)
        {
            if (lightsColor[i] == 2)
            {
                //Debug.Log("Green");
                GameObject tLight = Instantiate(greenLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
            else if (lightsColor[i] == 1)
            {
                //Debug.Log("Yellow");
                GameObject tLight = Instantiate(yellowLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
            else if (lightsColor[i] == 0)
            {
                //Debug.Log("Red");
                GameObject tLight = Instantiate(redLightPrefab, traficLightPositions[i], Quaternion.identity);
                Lights.Add(tLight);
            }
        }
    }
    void InnitAgents()
    {
        //Create the lights
        lightsColor = new List<int>(newLights);
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
        //Create the cars
        carPositions = new Dictionary<int, Vector3>(newCarPositions);

        foreach (var carPosition in carPositions)
        {
            //choose ramndomly a car prefab
            //int carPrefabIndex = UnityEngine.Random.Range(0, carPrefabs.Count);
            //GameObject carPrefab = carPrefabs[carPrefabIndex];

            //Instantiate the car
            GameObject newCar = Instantiate(carPrefab, carPositions[carPosition.Key], Quaternion.identity);
            carAgents[carPosition.Key] = newCar;
        }

    }

    void UpdateCars()
    {
        //check if the car exists in carPositions
        foreach (var car in newCarPositions)
        {
            //if the car exists both in new and existing cars, update its position
            if (carPositions.ContainsKey(car.Key))
            {
                //Debug.Log("Update car");
                //carAgents[car.Key].transform.position = Vector3.Lerp(carPositions[car.Key], car.Value, dt);
                carAgents[car.Key].transform.position = car.Value;
                carPositions[car.Key] = car.Value;
            }
            //if the car doesn't exist in carPositions, but it exists in newCarPositions, create it
            else
            {
                //if the car doesn't exist, create it
                //choose ramndomly a car prefab
                //int carPrefabIndex = UnityEngine.Random.Range(0, carPrefabs.Count);
                //GameObject carPrefab = carPrefabs[carPrefabIndex];

                //Instantiate the car
                Debug.Log("Create new car");
                GameObject newCar = Instantiate(carPrefab, car.Value, Quaternion.identity);
                carAgents[car.Key] = newCar;
                carPositions[car.Key] = car.Value;
            }
        }
        //if the car doesn't exist in newCarPositions, but it exists in carPositions, destroy it
        List<int> carsToDestroy = new List<int>();
        foreach (var car2 in carPositions)
        {
            if (!newCarPositions.ContainsKey(car2.Key))
            {
                Debug.Log("Car to destroy: "+car2.Key);
                carsToDestroy.Add(car2.Key);
            }
        }
        foreach (var car3 in carsToDestroy)
        {
            Debug.Log("Destroy car");
            Destroy(carAgents[car3]);
            carAgents.Remove(car3);
            carPositions.Remove(car3);
        }
    }

}
