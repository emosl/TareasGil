using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    //Agregamos las ruegas
    [SerializeField] Vector3 displacement;
    // [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;

    [SerializeField] GameObject wheel1;
    [SerializeField] GameObject wheel2;
    [SerializeField] GameObject wheel3;
    [SerializeField] GameObject wheel4;

    [SerializeField] float wheelRotationSpeed;


    // Mallas y vértices para el coche y las ruedas
    Mesh mesh;
    Mesh meshWheel1;
    Mesh meshWheel2;
    Mesh meshWheel3;
    Mesh meshWheel4;

    Vector3[] baseVertices;
    Vector3[] newVertices;

    Vector3[] baseVertices1;
    Vector3[] newVertices1;

    Vector3[] baseVertices2;
    Vector3[] newVertices2;

    Vector3[] baseVertices3;
    Vector3[] newVertices3;

    Vector3[] baseVertices4;
    Vector3[] newVertices4;

    void Start()
    {
        // Inicialización de mallas y vértices
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;
        newVertices = new Vector3[baseVertices.Length];

        meshWheel1 = wheel1.GetComponentInChildren<MeshFilter>().mesh;
        baseVertices1 = meshWheel1.vertices;
        newVertices1 = new Vector3[baseVertices1.Length];

        meshWheel2 = wheel2.GetComponentInChildren<MeshFilter>().mesh;
        baseVertices2 = meshWheel2.vertices;
        newVertices2 = new Vector3[baseVertices2.Length];

        meshWheel3 = wheel3.GetComponentInChildren<MeshFilter>().mesh;
        baseVertices3 = meshWheel3.vertices;
        newVertices3 = new Vector3[baseVertices3.Length];

        meshWheel4 = wheel4.GetComponentInChildren<MeshFilter>().mesh;
        baseVertices4 = meshWheel4.vertices;
        newVertices4 = new Vector3[baseVertices4.Length];
    }


    void Update()
    {
        DoTransform(mesh, baseVertices);

    }

   void DoTransform(Mesh mesh, Vector3[] vertices)
    {
        // Cálculos para la rotación y desplazamiento
        float angleRadians = Mathf.Atan2(displacement.z, displacement.x);

        float angle = angleRadians * Mathf.Rad2Deg-90;
        Debug.Log("Rotation Angle: " + angle);

        // Creación de matrices para diferentes transformaciones
        
        Matrix4x4 move= HW_Transforms.TranslationMat(displacement.x *Time.time , displacement.y *Time.time, displacement.z *Time.time);

        Matrix4x4 moveOrigin= HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);

        Matrix4x4 moveObject= HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);

        Matrix4x4 rotate = HW_Transforms.RotateMat(angle , rotationAxis );
        Matrix4x4 wheelRotate = HW_Transforms.RotateMat(Time.time * wheelRotationSpeed, AXIS.X);
        
        // Composición de transformaciones
        Matrix4x4 composite =   move * rotate;
        
        // Matrices de posición y escala para las ruedas
        Matrix4x4 pos1 = HW_Transforms.TranslationMat(1.02f, 0.23f, 1.71f );
        Matrix4x4 pos2 = HW_Transforms.TranslationMat(1.02f, 0.27f, -1.42f );
        Matrix4x4 pos3 = HW_Transforms.TranslationMat(-1.02f, 0.27f, -1.42f );
        Matrix4x4 pos4 = HW_Transforms.TranslationMat(-1.02f, 0.23f, 1.71f );

        Matrix4x4 sclae = HW_Transforms.ScaleMat(0.4f,0.4f,0.4f);

        Matrix4x4 rot = HW_Transforms.RotateMat(-90, AXIS.Y);

        // Aplicación de las transformaciones a los vértices
        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp ;
        }

        for (int i = 0; i < newVertices1.Length; i++)
        {
            Vector4 temp1 = new Vector4(baseVertices1[i].x, baseVertices1[i].y, baseVertices1[i].z, 1);
            newVertices1[i] = composite  * pos1  * wheelRotate * sclae *  temp1;
        }

        for (int i = 0; i < newVertices2.Length; i++)
        {
            Vector4 temp2 = new Vector4(baseVertices2[i].x, baseVertices2[i].y, baseVertices2[i].z, 1);
            newVertices2[i] = composite  * pos2 * wheelRotate * sclae * temp2;
        }

        for (int i = 0; i < newVertices3.Length; i++)
        {
            Vector4 temp3 = new Vector4(baseVertices3[i].x, baseVertices3[i].y, baseVertices3[i].z, 1);
            newVertices3[i] = composite  * pos3 * wheelRotate * sclae * temp3;
        }
        for (int i = 0; i < newVertices4.Length; i++)
        {
            Vector4 temp4 = new Vector4(baseVertices4[i].x, baseVertices4[i].y, baseVertices4[i].z, 1);
            newVertices4[i] = composite  * pos4 * wheelRotate * sclae * temp4;
        }


        // Actualización de las mallas con los nuevos vértices y recalculación de normales
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();

        meshWheel1.vertices = newVertices1;
        meshWheel1.RecalculateNormals();

        meshWheel2.vertices = newVertices2;
        meshWheel2.RecalculateNormals();

        meshWheel3.vertices = newVertices3;
        meshWheel3.RecalculateNormals();

        meshWheel4.vertices = newVertices4;
        meshWheel4.RecalculateNormals();
    }
}


